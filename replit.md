# Mini World Mod Generator

## Overview

This is a Flask-based web application that generates mod files for Mini World, a popular mobile game. The application allows users to create custom mod files by selecting creatures, setting IDs, and providing author information. It generates ZIP files containing the necessary mod files for the game.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes (2025-07-16)

✅ **Modern Navbar Implementation**: Added sticky navigation bar with blur effect and modern styling
✅ **Enhanced UI/UX**: Updated hero section with gradient backgrounds and modern badges
✅ **Desktop Application**: Created standalone desktop tool with complete GUI (desktop_app.py)
✅ **Download Functionality**: Added desktop tool download route and JavaScript handling
✅ **Responsive Design**: Improved mobile experience with responsive CSS
✅ **Modal System**: Added About and Guide modals with accordion-style help content
✅ **Modern Styling**: Updated color scheme with modern gradients and shadows

## System Architecture

### Frontend Architecture
- **Framework**: Pure HTML/CSS/JavaScript with Bootstrap 5 for responsive design
- **Styling**: Custom CSS with CSS variables for theming and modern design patterns
- **JavaScript**: Vanilla JavaScript for form handling, validation, and UI interactions
- **UI Components**: Bootstrap modals, forms, and alerts for user feedback

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **Structure**: Simple MVC pattern with separate modules for mod generation logic
- **Session Management**: Flask sessions with configurable secret key
- **Proxy Support**: ProxyFix middleware for deployment behind reverse proxies

### Key Components
1. **Flask App** (`app.py`): Main application with routing and request handling
2. **Mod Generator** (`mod_generator.py`): Core business logic for creating mod files
3. **Templates**: Jinja2 templates for rendering HTML pages
4. **Static Assets**: CSS and JavaScript files for frontend functionality

## Data Flow

1. User visits the main page and sees a form with creature selection dropdown
2. User fills out the form with:
   - Creature selection (from predefined list)
   - Custom ID value
   - Author name
3. Form submission triggers mod generation process
4. Backend creates temporary files and packages them into a ZIP
5. User receives download link for the generated mod files

## Key Components

### Mod Generation Logic
- **Creature Data**: Hardcoded list of creatures with their IDs and names
- **File Generation**: Creates JSON files for mod configuration and ride settings
- **Packaging**: Combines generated files into a downloadable ZIP archive
- **Temporary File Management**: Uses Python's tempfile module for secure file handling

### Data Structure
- **Creature Database**: Pipe-separated text data parsed into dictionary format
- **Mod Files**: JSON structure containing:
  - PhysicsActor configurations
  - Avatar information
  - Foreign IDs
  - Mod metadata (author, filename, UUID, version)
  - Property settings (copyid, id)
  - AI settings

### User Interface Features
- **Responsive Design**: Mobile-first approach with Bootstrap
- **Form Validation**: Client-side and server-side validation
- **Progress Indicators**: Loading states and success/error messages
- **File Download**: Direct ZIP file download functionality

## External Dependencies

### Python Packages
- **Flask**: Web framework for handling HTTP requests
- **Werkzeug**: WSGI utilities including ProxyFix middleware
- **Standard Library**: tempfile, zipfile, datetime, json, uuid, random, string, os, shutil

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive design
- **Font Awesome**: Icon library for UI elements
- **Modern CSS**: Custom styling with CSS variables and gradients

## Deployment Strategy

### Environment Configuration
- **Session Secret**: Configurable via environment variable with fallback
- **Debug Mode**: Configured through logging module
- **Static Files**: Served through Flask's static file handling

### File Management
- **Temporary Files**: Created in system temp directory and cleaned up after use
- **ZIP Archives**: Generated on-demand and served directly to user
- **No Persistent Storage**: All generated files are temporary and not stored long-term

### Security Considerations
- **Input Validation**: Form data validation on both client and server side
- **File Handling**: Secure temporary file creation and cleanup
- **Session Management**: Proper session secret configuration
- **XSS Protection**: Template escaping through Jinja2

### Architecture Decisions

**Problem**: Need to generate custom mod files for Mini World game
**Solution**: Web-based generator with form interface and ZIP download
**Rationale**: Provides user-friendly interface while maintaining security through server-side generation

**Problem**: Managing creature data and mod configurations
**Solution**: Hardcoded creature database with structured JSON output
**Rationale**: Simple maintenance and reliable data structure for game compatibility

**Problem**: File delivery to users
**Solution**: Temporary file generation with direct ZIP download
**Rationale**: No need for persistent storage, immediate file delivery, automatic cleanup

**Problem**: User experience on mobile devices
**Solution**: Responsive design with Bootstrap and mobile-optimized UI
**Rationale**: Target audience likely uses mobile devices, modern web standards