import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from mod_generator import ModGenerator
import tempfile
import zipfile
import shutil
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key-for-development")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize mod generator
mod_gen = ModGenerator()

@app.route('/')
def index():
    """Main page with the mod generator form"""
    # Create sorted list of creatures for dropdown
    creatures_list = []
    for copy_id, name in sorted(mod_gen.creature_data.items()):
        creatures_list.append((copy_id, name))
    
    return render_template('index.html', creatures=creatures_list)

@app.route('/generate', methods=['POST'])
def generate_mod():
    """Generate mod files and return download link"""
    try:
        # Get form data
        id_value = request.form.get('id_value', type=int)
        creature_select = request.form.get('creature_select', type=int)
        author_value = request.form.get('author_value', '').strip()
        
        # Validation
        if not author_value:
            flash('Tên tác giả là bắt buộc', 'error')
            return redirect(url_for('index'))
        
        if not id_value:
            flash('ID là bắt buộc', 'error')
            return redirect(url_for('index'))
            
        if not creature_select:
            flash('Chọn thần thú là bắt buộc', 'error')
            return redirect(url_for('index'))
        
        # Get creature name
        item_name = mod_gen.creature_data.get(creature_select, 'Unknown Creature')
        
        # Generate files
        result = mod_gen.generate_files(
            id_value=id_value,
            copyid_value=creature_select,
            author_value=author_value,
            item_name=item_name
        )
        
        if not result:
            flash('Failed to generate mod files', 'error')
            return redirect(url_for('index'))
        
        # Create temporary directory for files
        temp_dir = tempfile.mkdtemp(prefix='miniworld_mod_')
        
        # Create organized folder structure
        folders = {
            'actor': 'Actor',
            'horse': 'Horse', 
            'crafting': 'Crafting',
            'item': 'Item'
        }
        
        # Create subdirectories
        for folder_name in folders.values():
            os.makedirs(os.path.join(temp_dir, folder_name), exist_ok=True)
        
        # Write files to organized directories
        file_paths = []
        for filename, (content, file_type) in result['files'].items():
            folder_name = folders.get(file_type, 'Other')
            file_path = os.path.join(temp_dir, folder_name, filename)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            file_paths.append(file_path)
        
        # Create ZIP file with copyid + creature name
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Clean creature name for filename (remove special characters)
        clean_name = ''.join(c for c in item_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        clean_name = clean_name.replace(' ', '_')
        zip_filename = f'{creature_select}_{clean_name}.zip'
        zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                # Get relative path from temp_dir to maintain folder structure
                relative_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, relative_path)
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        # Store both files and zip path for preview/download
        session_key = f'files_{timestamp}'
        
        # Store file data and metadata
        file_data = {
            'files': result['files'],
            'zip_path': zip_path,
            'metadata': {
                'id_value': id_value,
                'creature_select': creature_select,
                'author_value': author_value,
                'item_name': item_name,
                'timestamp': timestamp,
                'zip_filename': zip_filename
            }
        }
        
        app.config[session_key] = file_data
        
        flash(f'Tạo file mod thành công! Files: {", ".join(result["files"].keys())}', 'success')
        
        return jsonify({
            'success': True,
            'session_key': session_key,
            'files_generated': list(result['files'].keys()),
            'file_details': [
                {
                    'name': filename,
                    'type': file_type,
                    'size': len(content)
                }
                for filename, (content, file_type) in result['files'].items()
            ],
            'metadata': file_data['metadata'],
            'download_zip_url': url_for('download_zip', session_key=session_key)
        })
        
    except Exception as e:
        app.logger.error(f'Error generating mod: {str(e)}')
        flash(f'Error generating mod: {str(e)}', 'error')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_zip/<session_key>')
def download_zip(session_key):
    """Download the generated ZIP file"""
    try:
        file_data = app.config.get(session_key)
        if not file_data or not os.path.exists(file_data['zip_path']):
            flash('File ZIP không tồn tại hoặc đã hết hạn', 'error')
            return redirect(url_for('index'))
        
        zip_path = file_data['zip_path']
        filename = file_data['metadata']['zip_filename']
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        app.logger.error(f'Error downloading ZIP: {str(e)}')
        flash(f'Lỗi tải file ZIP: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/preview/<session_key>')
def preview_files(session_key):
    """Preview generated files"""
    try:
        file_data = app.config.get(session_key)
        if not file_data:
            return jsonify({'error': 'Session đã hết hạn'}), 404
        
        files_info = []
        for filename, (content, file_type) in file_data['files'].items():
            files_info.append({
                'name': filename,
                'type': file_type,
                'size': len(content),
                'content': content[:500] + '...' if len(content) > 500 else content,
                'full_content': content
            })
        
        return jsonify({
            'success': True,
            'files': files_info,
            'metadata': file_data['metadata']
        })
        
    except Exception as e:
        app.logger.error(f'Error previewing files: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/download_single/<session_key>/<filename>')
def download_single_file(session_key, filename):
    """Download a single file"""
    try:
        file_data = app.config.get(session_key)
        if not file_data:
            flash('Session đã hết hạn', 'error')
            return redirect(url_for('index'))
        
        if filename not in file_data['files']:
            flash('File không tồn tại', 'error')
            return redirect(url_for('index'))
        
        content, file_type = file_data['files'][filename]
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.json',
            delete=False,
            encoding='utf-8'
        )
        temp_file.write(content)
        temp_file.close()
        
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        app.logger.error(f'Error downloading single file: {str(e)}')
        flash(f'Lỗi tải file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/get_creature_info/<int:copyid>')
def get_creature_info(copyid):
    """Get creature information by copy ID"""
    creature_name = mod_gen.creature_data.get(copyid, 'Unknown Creature')
    return jsonify({'name': creature_name})

@app.route('/auto_generate', methods=['POST'])
def auto_generate():
    """Auto generate files for all creatures"""
    try:
        author_value = request.form.get('author_value', '').strip()
        
        if not author_value:
            return jsonify({'success': False, 'error': 'Tên tác giả là bắt buộc'})
        
        # Create temporary directory for all files
        temp_dir = tempfile.mkdtemp(prefix='miniworld_auto_mod_')
        
        # Create organized folder structure
        folders = {
            'actor': 'Actor',
            'horse': 'Horse', 
            'crafting': 'Crafting',
            'item': 'Item'
        }
        
        # Create subdirectories
        for folder_name in folders.values():
            os.makedirs(os.path.join(temp_dir, folder_name), exist_ok=True)
        
        # Generate files for highest level creatures only
        current_id = mod_gen.auto_id_counter
        total_files = 0
        all_files = []
        
        # Get grouped creatures (highest level only)
        highest_level_creatures = mod_gen.group_creatures_by_level()
        
        for copy_id, creature_name in sorted(highest_level_creatures.items()):
            result = mod_gen.generate_files(
                id_value=current_id,
                copyid_value=copy_id,
                author_value=author_value,
                item_name=creature_name
            )
            
            if result:
                # Write files to organized directories
                for filename, (content, file_type) in result['files'].items():
                    folder_name = folders.get(file_type, 'Other')
                    file_path = os.path.join(temp_dir, folder_name, filename)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    all_files.append(file_path)
                    total_files += 1
                    
                current_id += 1
        
        # Update auto counter
        mod_gen.auto_id_counter = current_id
        
        # Create ZIP file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_filename = f'miniworld_auto_mod_{author_value}_{timestamp}.zip'
        zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in all_files:
                # Get relative path from temp_dir to maintain folder structure
                relative_path = os.path.relpath(file_path, temp_dir)
                zipf.write(file_path, relative_path)
        
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        
        # Store zip path for download
        session_key = f'auto_files_{timestamp}'
        
        # Store auto generation data
        auto_data = {
            'zip_path': zip_path,
            'total_files': total_files,
            'total_creatures': len(mod_gen.creature_data),
            'metadata': {
                'author_value': author_value,
                'timestamp': timestamp,
                'zip_filename': zip_filename
            }
        }
        
        app.config[session_key] = auto_data
        
        return jsonify({
            'success': True,
            'session_key': session_key,
            'filename': zip_filename,
            'total_files': total_files,
            'total_creatures': len(highest_level_creatures),
            'download_url': url_for('download_zip', session_key=session_key)
        })
        
    except Exception as e:
        app.logger.error(f'Error in auto generate: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/reset_counters', methods=['POST'])
def reset_counters():
    """Reset auto ID counters to default values"""
    try:
        mod_gen.auto_id_counter = 2
        mod_gen.auto_result_id_counter = 4097
        
        return jsonify({
            'success': True,
            'message': 'Đã reset ID và Result ID về mặc định',
            'auto_id_counter': mod_gen.auto_id_counter,
            'auto_result_id_counter': mod_gen.auto_result_id_counter
        })
        
    except Exception as e:
        app.logger.error(f'Error resetting counters: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_desktop')
def download_desktop():
    """Download desktop tool"""
    try:
        desktop_file = os.path.join(app.static_folder or 'static', 'MiniWorldModGenerator.exe')
        if os.path.exists(desktop_file):
            return send_file(desktop_file, as_attachment=True, download_name='MiniWorldModGenerator.exe')
        else:
            flash('Desktop tool không tìm thấy', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(f'Error downloading desktop tool: {str(e)}')
        flash(f'Lỗi tải desktop tool: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download_source')
def download_source():
    """Download complete source code as ZIP"""
    try:
        import zipfile
        from datetime import datetime
        
        # Tạo file ZIP trong thư mục tạm
        zip_filename = f'miniworld_mod_generator_source_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        zip_path = os.path.join(tempfile.gettempdir(), zip_filename)
        
        # Các file và thư mục cần đưa vào ZIP
        source_files = [
            'app.py',
            'main.py', 
            'mod_generator.py',
            'desktop_app.py',
            'replit.md',
            'templates/',
            'static/'
        ]
        
        # Thư mục gốc của dự án
        project_root = os.path.dirname(os.path.abspath(__file__))
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in source_files:
                item_path = os.path.join(project_root, item)
                
                if os.path.isfile(item_path):
                    # Thêm file đơn lẻ
                    zipf.write(item_path, item)
                    
                elif os.path.isdir(item_path):
                    # Thêm toàn bộ thư mục
                    for root, dirs, files in os.walk(item_path):
                        for file in files:
                            file_path = os.path.join(root, file)
                            # Tạo đường dẫn tương đối trong ZIP
                            arcname = os.path.relpath(file_path, project_root)
                            zipf.write(file_path, arcname)
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=zip_filename,
            mimetype='application/zip'
        )
        
    except Exception as e:
        app.logger.error(f'Error creating source ZIP: {str(e)}')
        flash(f'Lỗi tạo file ZIP mã nguồn: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', creatures=mod_gen.creature_groups), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f'Internal error: {str(error)}')
    flash('An internal error occurred. Please try again.', 'error')
    return render_template('index.html', creatures=mod_gen.creature_groups), 500

if __name__ == '__main__':
    # Ensure temp directory exists
    os.makedirs('temp', exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
