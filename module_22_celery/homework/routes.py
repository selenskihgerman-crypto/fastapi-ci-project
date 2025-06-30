from flask import Blueprint, request, jsonify
from app import db
from app.models import Subscriber
from app.tasks import process_image, send_processed_images
from celery import chord
import uuid
import os

bp = Blueprint('api', __name__)


@bp.route('/blur', methods=['POST'])
def process_images():
    """Endpoint to start image processing"""
    if 'images' not in request.files:
        return jsonify({'error': 'No images provided'}), 400

    email = request.form.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400

    # Save uploaded files
    image_paths = []
    processed_paths = []
    for file in request.files.getlist('images'):
        if not file.filename:
            continue

        filename = f"{uuid.uuid4()}_{file.filename}"
        orig_path = os.path.join('uploads', filename)
        proc_path = os.path.join('processed', filename)

        file.save(orig_path)
        image_paths.append(orig_path)
        processed_paths.append(proc_path)

    # Create processing chord
    processing_tasks = [process_image.s(p[0], p[1]) for p in zip(image_paths, processed_paths)]
    result = chord(processing_tasks)(send_processed_images.s(email, processed_paths))

    return jsonify({
        'task_id': result.id,
        'message': f'Processing {len(image_paths)} images'
    }), 202


@bp.route('/status/<task_id>')
def check_status(task_id):
    """Check task status"""
    from celery.result import AsyncResult
    from app.extensions import celery

    result = AsyncResult(task_id, app=celery)
    return jsonify({
        'status': result.status,
        'ready': result.ready()
    })


@bp.route('/subscribe', methods=['POST'])
def subscribe():
    """Subscribe email to newsletter"""
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400

    subscriber = Subscriber.query.filter_by(email=email).first() or Subscriber(email=email)
    subscriber.is_active = True
    db.session.add(subscriber)
    db.session.commit()

    return jsonify({'message': 'Subscribed successfully'})


@bp.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    """Unsubscribe email"""
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email required'}), 400

    if subscriber := Subscriber.query.filter_by(email=email).first():
        subscriber.is_active = False
        db.session.commit()
        return jsonify({'message': 'Unsubscribed'})

    return jsonify({'error': 'Email not found'}), 404