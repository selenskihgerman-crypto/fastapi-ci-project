from celery import shared_task, chord
from PIL import Image, ImageFilter
from app import create_app, mail
from flask_mail import Message
import os
import zipfile
import io

app = create_app()


@shared_task(bind=True)
def process_image(self, image_path, output_path):
    """Apply blur effect to single image"""
    try:
        with Image.open(image_path) as img:
            blurred = img.filter(ImageFilter.GaussianBlur(radius=5))
            blurred.save(output_path)
        os.remove(image_path)  # Cleanup original
        return output_path
    except Exception as e:
        self.retry(exc=e, countdown=60)


@shared_task
def send_processed_images(email, processed_paths):
    """Send email with all processed images"""
    with app.app_context():
        try:
            # Create in-memory zip
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w') as zf:
                for path in processed_paths:
                    if os.path.exists(path):
                        zf.write(path, os.path.basename(path))

            # Prepare email
            msg = Message(
                "Your Processed Images",
                recipients=[email],
                body="Attached are your blurred images."
            )
            msg.attach("images.zip", "application/zip", zip_buffer.getvalue())

            mail.send(msg)

            # Cleanup processed files
            for path in processed_paths:
                if os.path.exists(path):
                    os.remove(path)

            return True
        except Exception as e:
            app.logger.error(f"Email failed: {str(e)}")
            return False


@shared_task
def weekly_newsletter():
    """Send weekly digest to subscribers"""
    with app.app_context():
        from app.models import Subscriber
        for sub in Subscriber.query.filter_by(is_active=True).all():
            msg = Message(
                "Weekly Image Service Digest",
                recipients=[sub.email],
                body="Latest updates from our service..."
            )
            mail.send(msg)