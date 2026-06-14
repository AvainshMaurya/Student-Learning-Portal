# Student Learning Portal - Installation & Setup Guide

## Quick Start Guide

This guide will help you set up and run the Student Learning Portal on your system.

---

## System Requirements

- **Python**: 3.9 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: Minimum 2GB
- **Storage**: 500MB free space
- **Browser**: Modern browser (Chrome, Firefox, Safari, Edge)

---

## Installation Steps

### Step 1: Extract/Prepare the Project

```bash
# Navigate to the project directory
cd StudentLearningPortal
```

### Step 2: Create Python Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Upgrade pip

```bash
# Upgrade pip to latest version
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

---

## First Run Setup

1. **Access the Application**: Open browser and go to `http://localhost:5000`
2. **Database Initialization**: Database creates automatically on first run
3. **Sample Data**: Demo quizzes and materials are pre-loaded
4. **Login with Demo Account**:
   - Username: `student1`
   - Password: `password123`

---

## Project Structure Navigation

After installation, your directory will look like:

```
StudentLearningPortal/
├── app.py                  # Main application file
├── requirements.txt        # Dependencies
├── README.md              # Main documentation
│
├── templates/             # HTML pages
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── [more templates...]
│
├── static/               # CSS, JS, Images
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── images/
│
└── docs/                 # Documentation

```

---

## Configuration

### Change Application Port

Edit `app.py` and modify the last line:

```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change 5000 to 5001
```

### Change Secret Key (Important for Production)

```python
app.config['SECRET_KEY'] = 'your-new-secret-key-here'
```

---

## Features Available After Setup

✅ User Registration and Login
✅ Student Dashboard with Statistics
✅ Study Materials (with download capability)
✅ Video Learning Section
✅ Interactive Quizzes
✅ Score Tracking and Results
✅ Progress Analytics
✅ Certificate Generation (PDF)
✅ Dark Mode Toggle
✅ Responsive Mobile Design
✅ Contact/Feedback Form
✅ About Page with SDG 4 Information

---

## Demo Credentials

### Student Account
- Username: `student1`
- Password: `password123`
- Full Name: John Doe

### Alternative Student
- Username: `student2`
- Password: `password123`
- Full Name: Jane Smith

---

## Database Information

- **Database File**: `student_portal.db` (created in project root)
- **Type**: SQLite
- **Size**: ~100KB (with sample data)
- **Tables**: 7 main tables

To reset the database:
1. Delete `student_portal.db` file
2. Run `python app.py` again
3. Database recreates with fresh data

---

## Troubleshooting

### Issue 1: Port 5000 Already in Use

```
Address already in use
```

**Solution**: Change the port number in `app.py` line:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue 2: Module Not Found Error

```
ModuleNotFoundError: No module named 'flask'
```

**Solution**: Install dependencies again:
```bash
pip install -r requirements.txt
```

### Issue 3: CSS/JS Not Loading

```
Static files appear broken
```

**Solution**:
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+F5)
- Check if static folder exists

### Issue 4: Database Error

```
sqlite3.OperationalError
```

**Solution**:
- Delete `student_portal.db`
- Restart the application
- Database will auto-initialize

### Issue 5: Virtual Environment Not Activated

```
'pip' is not recognized
```

**Solution**: Make sure virtual environment is activated:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

---

## Testing the Application

### Test 1: Registration
1. Click "Register" button
2. Fill in form with new credentials
3. Should redirect to login page

### Test 2: Login
1. Click "Login" button
2. Use credentials: student1 / password123
3. Should show dashboard

### Test 3: Quiz
1. Go to "Quizzes" section
2. Click "Start Quiz"
3. Answer questions and submit
4. View results

### Test 4: Materials
1. Go to "Study Materials"
2. Click "Download" button
3. Should download text file

---

## Browser Compatibility

| Browser | Version | Support |
|---------|---------|---------|
| Chrome | 90+ | ✅ Full |
| Firefox | 88+ | ✅ Full |
| Safari | 14+ | ✅ Full |
| Edge | 90+ | ✅ Full |
| IE | Any | ❌ Not Supported |

---

## Performance Tips

1. **Clear Browser Cache**: Speeds up page loading
2. **Use Modern Browser**: Better performance
3. **Close Unused Tabs**: Reduces system load
4. **Enable JavaScript**: Required for full functionality

---

## Development Tips

### Enable Debug Mode
Already enabled in `app.py`. Shows detailed error messages.

### View Database Contents
```bash
# Install sqlite3 tool
# Then
sqlite3 student_portal.db
.tables
SELECT * FROM user;
```

### Modify Sample Data
Edit the `init_db()` function in `app.py` to customize initial data.

---

## Deployment for Production

### Steps:
1. Set `debug=False` in app.py
2. Install production WSGI server:
   ```bash
   pip install gunicorn
   ```
3. Run with Gunicorn:
   ```bash
   gunicorn --bind 0.0.0.0:5000 app:app
   ```
4. Use reverse proxy (Nginx/Apache)
5. Enable HTTPS/SSL certificates
6. Setup environment variables

---

## Updating Dependencies

To update all packages to latest versions:

```bash
pip list --outdated
pip install --upgrade pip
pip install -r requirements.txt --upgrade
```

---

## Uninstallation

To remove the application:

1. Delete the project folder
2. Deactivate virtual environment:
   ```bash
   deactivate
   ```
3. Delete virtual environment folder

---

## Support & Documentation

- **Main Documentation**: See `README.md`
- **Contact Form**: Use in-app contact form for feedback
- **Issues**: Check troubleshooting section above

---

## Getting Started with Features

### Taking Your First Quiz:
1. Login to dashboard
2. Click "Take Quizzes" or go to Quizzes section
3. Select "Mathematics Quiz 1"
4. Answer 5 questions within time limit
5. Submit and see results
6. If passed, download certificate

### Tracking Progress:
1. Go to "Progress" from user menu
2. View statistics and score trends
3. See detailed quiz history
4. Monitor average performance

### Downloading Materials:
1. Go to "Study Materials"
2. Browse by category
3. Click "Download" button
4. File saves to downloads folder

---

## Additional Resources

- **Python Flask Documentation**: https://flask.palletsprojects.com/
- **Bootstrap Documentation**: https://getbootstrap.com/docs/
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/

---

## Frequently Asked Questions

**Q: How do I create a new quiz?**
A: Currently, quizzes are created in the backend. Admin panel coming soon.

**Q: Can I export my results?**
A: View results page shows all information. Print or screenshot as needed.

**Q: Is my data saved?**
A: Yes, all data is saved to SQLite database.

**Q: Can I change password?**
A: Feature coming in v2.0. Use contact form for password reset.

**Q: How do I backup my data?**
A: Copy the `student_portal.db` file to a safe location.

---

## Success Indicators

After successful setup, you should see:
✅ Home page loads with SDG 4 information
✅ Registration and login work
✅ Dashboard shows demo user info
✅ Sample quizzes are available
✅ Study materials can be downloaded
✅ Dark mode toggle functions
✅ Quiz timer works correctly
✅ Results display properly

---

## Next Steps

1. **Explore the Platform**: Test all features
2. **Customize Content**: Add your own materials and quizzes
3. **Invite Users**: Share with friends/colleagues
4. **Provide Feedback**: Use contact form for suggestions
5. **Track Progress**: Monitor learning outcomes

---

## Version Information

- **Current Version**: 1.0
- **Release Date**: 2024
- **Status**: Production Ready
- **License**: Educational Use

---

**Congratulations! You have successfully set up the Student Learning Portal. Happy Learning! 📚**

For support, please use the Contact Form on the platform.
