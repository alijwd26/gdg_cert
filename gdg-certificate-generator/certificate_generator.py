import os
import io
import json
import hashlib
from datetime import datetime
from typing import List, Tuple, Dict
from PIL import Image, ImageDraw, ImageFont
import qrcode
import img2pdf
import requests


class CertificateGenerator:
    """Core class for generating certificates with security features."""
    
    def __init__(self, template_path: str, event_name: str = "GDG Basra Event"):
        """
        Initialize the certificate generator.
        
        Args:
            template_path: Path to the certificate template image
            event_name: Name of the event for hash generation
        """
        self.template = Image.open(template_path)
        self.event_name = event_name
        self.template_width, self.template_height = self.template.size
        
    def download_google_font(self, font_name: str, font_dir: str = "fonts") -> str:
        """
        Download a Google Font if not already cached.
        
        Args:
            font_name: Name of the Google Font (e.g., 'Amiri', 'Roboto')
            font_dir: Directory to store downloaded fonts
            
        Returns:
            Path to the downloaded font file
        """
        os.makedirs(font_dir, exist_ok=True)
        font_path = os.path.join(font_dir, f"{font_name}.ttf")
        
        # If font already exists, return the path
        if os.path.exists(font_path):
            return font_path
        
        # Google Fonts API URL mappings for common fonts
        font_urls = {
            'Amiri': 'https://github.com/google/fonts/raw/main/ofl/amiri/Amiri-Regular.ttf',
            'Cairo': 'https://github.com/google/fonts/raw/main/ofl/cairo/Cairo%5Bwght%5D.ttf',
            'Roboto': 'https://github.com/google/fonts/raw/main/apache/roboto/static/Roboto-Regular.ttf',
            'OpenSans': 'https://github.com/google/fonts/raw/main/apache/opensans/OpenSans%5Bwdth%2Cwght%5D.ttf',
            'Montserrat': 'https://github.com/google/fonts/raw/main/ofl/montserrat/Montserrat%5Bwght%5D.ttf',
            'Tajawal': 'https://github.com/google/fonts/raw/main/ofl/tajawal/Tajawal-Regular.ttf',
            'Almarai': 'https://github.com/google/fonts/raw/main/ofl/almarai/Almarai-Regular.ttf',
        }
        
        if font_name in font_urls:
            try:
                response = requests.get(font_urls[font_name])
                response.raise_for_status()
                with open(font_path, 'wb') as f:
                    f.write(response.content)
                return font_path
            except Exception as e:
                print(f"Error downloading font {font_name}: {e}")
                return None
        
        return None
    
    def generate_hash(self, attendee_name: str) -> str:
        """
        Generate a unique SHA-256 hash for an attendee.
        
        Args:
            attendee_name: Name of the attendee
            
        Returns:
            SHA-256 hash string
        """
        timestamp = datetime.now().isoformat()
        data = f"{attendee_name}{self.event_name}{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_qr_code(self, attendee_name: str, cert_hash: str) -> Image.Image:
        """
        Generate a QR code with verification data.
        
        Args:
            attendee_name: Name of the attendee
            cert_hash: SHA-256 hash of the certificate
            
        Returns:
            PIL Image object of the QR code
        """
        verification_data = {
            "hash": cert_hash,
            "name": attendee_name,
            "event": self.event_name,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )
        qr.add_data(json.dumps(verification_data))
        qr.make(fit=True)
        
        return qr.make_image(fill_color="black", back_color="white")
    
    def generate_certificate(
        self,
        attendee_name: str,
        name_position: Tuple[int, int],
        font_path: str,
        font_size: int,
        text_color: Tuple[int, int, int],
        hash_position: Tuple[int, int] = None,
        qr_position: Tuple[int, int] = None,
        qr_size: int = 150
    ) -> Tuple[Image.Image, str]:
        """
        Generate a single certificate.
        
        Args:
            attendee_name: Name of the attendee
            name_position: (x, y) coordinates for name placement
            font_path: Path to the font file
            font_size: Size of the font
            text_color: RGB tuple for text color
            hash_position: (x, y) coordinates for hash placement (optional)
            qr_position: (x, y) coordinates for QR code placement (optional)
            qr_size: Size of the QR code in pixels
            
        Returns:
            Tuple of (generated certificate image, hash)
        """
        # Create a copy of the template
        cert = self.template.copy()
        draw = ImageDraw.Draw(cert)
        
        # Load font
        try:
            font = ImageFont.truetype(font_path, font_size)
            hash_font = ImageFont.truetype(font_path, max(12, font_size // 3))
        except Exception as e:
            print(f"Error loading font: {e}")
            font = ImageFont.load_default()
            hash_font = ImageFont.load_default()
        
        # Draw attendee name
        draw.text(name_position, attendee_name, font=font, fill=text_color)
        
        # Generate hash
        cert_hash = self.generate_hash(attendee_name)
        hash_display = f"ID: {cert_hash[:12].upper()}"
        
        # Draw hash if position provided
        if hash_position:
            draw.text(hash_position, hash_display, font=hash_font, fill=text_color)
        else:
            # Default position: bottom left
            default_hash_pos = (50, self.template_height - 100)
            draw.text(default_hash_pos, hash_display, font=hash_font, fill=text_color)
        
        # Generate and paste QR code
        qr_img = self.generate_qr_code(attendee_name, cert_hash)
        qr_img = qr_img.resize((qr_size, qr_size))
        
        if qr_position:
            cert.paste(qr_img, qr_position)
        else:
            # Default position: bottom right
            default_qr_pos = (self.template_width - qr_size - 50, self.template_height - qr_size - 50)
            cert.paste(qr_img, default_qr_pos)
        
        return cert, cert_hash
    
    def save_as_pdf(self, image: Image.Image, output_path: str):
        """
        Save an image as a PDF file.
        
        Args:
            image: PIL Image object
            output_path: Path for the output PDF file
        """
        # Convert image to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save as PDF
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        with open(output_path, 'wb') as f:
            f.write(img2pdf.convert(img_byte_arr.getvalue()))
    
    def batch_generate(
        self,
        attendees: List[str],
        output_dir: str,
        name_position: Tuple[int, int],
        font_path: str,
        font_size: int,
        text_color: Tuple[int, int, int],
        hash_position: Tuple[int, int] = None,
        qr_position: Tuple[int, int] = None,
        qr_size: int = 150,
        save_as_pdf: bool = True
    ) -> List[Dict]:
        """
        Generate certificates for multiple attendees.
        
        Args:
            attendees: List of attendee names
            output_dir: Directory to save generated certificates
            name_position: (x, y) coordinates for name placement
            font_path: Path to the font file
            font_size: Size of the font
            text_color: RGB tuple for text color
            hash_position: (x, y) coordinates for hash placement (optional)
            qr_position: (x, y) coordinates for QR code placement (optional)
            qr_size: Size of the QR code in pixels
            save_as_pdf: Whether to save as PDF (True) or PNG (False)
            
        Returns:
            List of dictionaries with certificate information
        """
        os.makedirs(output_dir, exist_ok=True)
        results = []
        
        for i, attendee in enumerate(attendees):
            cert, cert_hash = self.generate_certificate(
                attendee_name=attendee,
                name_position=name_position,
                font_path=font_path,
                font_size=font_size,
                text_color=text_color,
                hash_position=hash_position,
                qr_position=qr_position,
                qr_size=qr_size
            )
            
            # Save certificate
            safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in attendee)
            if save_as_pdf:
                output_path = os.path.join(output_dir, f"{safe_name}.pdf")
                self.save_as_pdf(cert, output_path)
            else:
                output_path = os.path.join(output_dir, f"{safe_name}.png")
                cert.save(output_path)
            
            results.append({
                'name': attendee,
                'hash': cert_hash,
                'path': output_path
            })
        
        return results
