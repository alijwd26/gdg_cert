# GDG Basra Certificate Generator 🎓

A powerful Python-based certificate generator built with Streamlit for GDG Basra events. Generate professional certificates with built-in security features including SHA-256 hashing and QR codes.

## Features ✨

- **📤 Template Upload**: Upload custom certificate templates (JPG/PNG)
- **📝 Flexible Data Input**: 
  - Manual text entry
  - CSV/Excel file upload
- **🎨 Smart Customization**:
  - Google Fonts support (English & Arabic)
  - Adjustable text position (X/Y coordinates)
  - Customizable font size and color
  - QR code and hash placement controls
- **🔐 Security Features**:
  - Unique SHA-256 hash for each certificate
  - QR code with embedded verification data (name, hash, event, timestamp)
- **👁️ Preview**: Preview certificates before bulk generation
- **🚀 Bulk Generation**: Generate all certificates as PDFs
- **📦 ZIP Download**: Download all certificates in a single ZIP file

## Installation 🛠️

### Option 1: Run Online (Recommended - No Installation!)

**Deploy to Streamlit Cloud for FREE** and use it online without installing Python!

👉 **[See DEPLOYMENT.md for detailed instructions](DEPLOYMENT.md)**

**Quick Steps:**
1. Create a free GitHub account
2. Upload this project to GitHub
3. Deploy on [Streamlit Cloud](https://share.streamlit.io) (free)
4. Get a shareable URL!

### Option 2: Run Locally (Requires Python)

1. **Clone or download this repository**

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage 🚀

1. **Start the application**:
```bash
streamlit run app.py
```

2. **Follow the steps in the app**:
   - **Tab 1**: Upload your certificate template
   - **Tab 2**: Add attendees (manual entry or CSV/Excel upload)
   - **Tab 3**: Customize font, colors, and positioning
   - **Tab 4**: Generate and download all certificates

## Data Input Format 📋

### Manual Entry
Enter one name per line:
```
John Doe
Jane Smith
أحمد محمد
```

### CSV/Excel Format
Create a file with names in the first column:
```csv
Name
John Doe
Jane Smith
أحمد محمد
```

## Supported Fonts 🔤

The app includes these Google Fonts with Arabic support:
- **Amiri** (Arabic)
- **Cairo** (Arabic)
- **Tajawal** (Arabic)
- **Almarai** (Arabic)
- **Roboto** (English)
- **OpenSans** (English)
- **Montserrat** (English)

## Security Features 🔐

Each certificate includes:
1. **SHA-256 Hash**: A unique identifier generated from attendee name, event name, and timestamp
2. **QR Code**: Contains verification data in JSON format:
```json
{
  "hash": "abc123...",
  "name": "John Doe",
  "event": "GDG Basra Event",
  "date": "2026-02-05 19:00:00"
}
```

This QR code can be scanned to verify certificate authenticity.

## Project Structure 📁

```
gdg-certificate-generator/
├── app.py                    # Main Streamlit application
├── certificate_generator.py  # Core certificate generation logic
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── temp/                     # Temporary files (auto-created)
    ├── uploads/              # Uploaded templates
    ├── generated/            # Generated certificates
    └── output/               # ZIP files
```

## Requirements 📦

- Python 3.7+
- streamlit
- Pillow (PIL)
- pandas
- openpyxl
- qrcode[pil]
- img2pdf
- requests

## Tips 💡

1. **Template Design**: Use high-resolution templates (at least 1920x1080) for best results
2. **Font Selection**: Arabic fonts (Amiri, Cairo, Tajawal) work best for bilingual certificates
3. **Positioning**: Use the preview feature to fine-tune text placement
4. **QR Code Size**: Larger QR codes (150-200px) are easier to scan

## Troubleshooting 🔧

- **Font not loading**: The app will automatically download Google Fonts on first use
- **Image quality issues**: Try increasing the template resolution
- **QR code not scanning**: Increase the QR code size or ensure good contrast

## License 📄

This project is open source and available for GDG Basra community use.

## Support 💬

For issues or questions, please contact the GDG Basra team.

---

Made with ❤️ for **GDG Basra**
