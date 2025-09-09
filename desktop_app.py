#!/usr/bin/env python3
"""
Mini World Mod Generator Desktop Application
Based on the attached_assets/outu1_1752708098771.py file
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import uuid
import random
import string
import os
import threading
import time
import zipfile
import tempfile
import shutil
from datetime import datetime

class FileGeneratorThread(threading.Thread):
    def __init__(self, id_value, copyid_value, author_value, item_name, start_result_id, callback):
        super().__init__()
        self.id_value = id_value
        self.copyid_value = copyid_value
        self.author_value = author_value
        self.item_name = item_name
        self.start_result_id = start_result_id
        self.callback = callback
        self.daemon = True
        
    def run(self):
        time.sleep(0.5)
        
        random_filename = ''.join(random.choices(string.digits, k=10))
        uuid_value = str(uuid.uuid4())
        
        # Main mod file
        main_mod_data = {
            "PhysicsActor": [],
            "avatarInfo": [],
            "foreign_ids": [],
            "mod_desc": {
                "author": self.author_value,
                "filename": random_filename,
                "uuid": uuid_value,
                "version": "1"
            },
            "property": {
                "copyid": self.copyid_value,
                "id": self.id_value
            },
            "set_ai": [{"name": "swimming", "priority": 1}]
        }
        
        # Ride file
        ride_data = {
            "property": {
                "id": self.id_value,
                "copyid": self.copyid_value
            }
        }
        
        # Crafting file
        crafting_data = {
            "PhysicsActor": [],
            "avatarInfo": [],
            "foreign_ids": [
                {
                    "id": self.start_result_id,
                    "key": f"{self.author_value}{uuid_value.replace('-', '')}{random_filename}"
                }
            ],
            "mod_desc": {
                "author": self.author_value,
                "filename": ''.join(random.choices(string.digits, k=10)),
                "uuid": uuid_value,
                "version": "1"
            },
            "property": {
                "CraftingItemID": 11000,
                "copyid": self.copyid_value,
                "id": self.start_result_id + 1,
                "material_count1": 1,
                "material_count2": 0,
                "material_count3": 0,
                "material_count4": 0,
                "material_count5": 0,
                "material_count6": 0,
                "material_count7": 0,
                "material_count8": 0,
                "material_count9": 0,
                "material_count10": 0,
                "material_id1": 22,
                "material_id2": 0,
                "material_id3": 0,
                "material_id4": 0,
                "material_id5": 0,
                "material_id6": 0,
                "material_id7": 0,
                "material_id8": 0,
                "material_id9": 0,
                "material_id10": 0,
                "result_count": 1,
                "result_id": self.start_result_id
            }
        }
        
        # Prepare data for callback
        data = {
            'id': self.id_value,
            'copyid': self.copyid_value,
            'author': self.author_value,
            'item_name': self.item_name,
            'files': {
                f'{self.id_value}.json': json.dumps(main_mod_data, indent=2),
                f'{self.id_value}_ride.json': json.dumps(ride_data, indent=2),
                f'{self.id_value}_crafting.json': json.dumps(crafting_data, indent=2)
            }
        }
        
        self.callback(data)

class CompactModGenerator:
    def __init__(self):
        self.creature_data = {}
        self.creature_groups = {}
        self.auto_id_counter = 2
        self.auto_result_id_counter = 4097
        self.folder_path = os.path.join(os.path.expanduser("~"), "Desktop")
        self.last_generated_files = []
        
        self.load_creature_data()
        self.group_creatures_by_level()
        self.setup_ui()
        
    def load_creature_data(self):
        """Load creature data from the provided list"""
        creature_list = """
4533|Chó con (Cấp 1)
4534|Chó con (Cấp 2)
4535|Chó con (Cấp 3)
4536|Chó con (Cấp 4)
4537|Chó con (Cấp 5)
4538|Chó con (Cấp 6)
4539|Chó con (Cấp 7)
4540|Chó con (Cấp 8)
4541|Chó con (Cấp 9)
4542|Chó con (Cấp 10)
4543|Chó ma (Cấp 1)
4544|Chó ma (Cấp 2)
4545|Chó ma (Cấp 3)
4546|Chó ma (Cấp 4)
4547|Chó ma (Cấp 5)
4548|Chó ma (Cấp 6)
4549|Chó ma (Cấp 7)
4550|Chó ma (Cấp 8)
4551|Chó ma (Cấp 9)
4552|Chó ma (Cấp 10)
4553|Chó sói (Cấp 1)
4554|Chó sói (Cấp 2)
4555|Chó sói (Cấp 3)
4556|Chó sói (Cấp 4)
4557|Chó sói (Cấp 5)
4558|Chó sói (Cấp 6)
4559|Chó sói (Cấp 7)
4560|Chó sói (Cấp 8)
4561|Chó sói (Cấp 9)
4562|Chó sói (Cấp 10)
4563|Mèo con (Cấp 1)
4564|Mèo con (Cấp 2)
4565|Mèo con (Cấp 3)
4566|Mèo con (Cấp 4)
4567|Mèo con (Cấp 5)
4568|Mèo con (Cấp 6)
4569|Mèo con (Cấp 7)
4570|Mèo con (Cấp 8)
4571|Mèo con (Cấp 9)
4572|Mèo con (Cấp 10)
4573|Mèo ma (Cấp 1)
4574|Mèo ma (Cấp 2)
4575|Mèo ma (Cấp 3)
4576|Mèo ma (Cấp 4)
4577|Mèo ma (Cấp 5)
4578|Mèo ma (Cấp 6)
4579|Mèo ma (Cấp 7)
4580|Mèo ma (Cấp 8)
4581|Mèo ma (Cấp 9)
4582|Mèo ma (Cấp 10)
4583|Mèo hoang (Cấp 1)
4584|Mèo hoang (Cấp 2)
4585|Mèo hoang (Cấp 3)
4586|Mèo hoang (Cấp 4)
4587|Mèo hoang (Cấp 5)
4588|Mèo hoang (Cấp 6)
4589|Mèo hoang (Cấp 7)
4590|Mèo hoang (Cấp 8)
4591|Mèo hoang (Cấp 9)
4592|Mèo hoang (Cấp 10)
        """
        
        for line in creature_list.strip().split('\n'):
            if '|' in line:
                copy_id, name = line.split('|', 1)
                self.creature_data[int(copy_id)] = name.strip()
    
    def group_creatures_by_level(self):
        """Group creatures by their base name and return the highest level for each"""
        groups = {}
        for copy_id, name in self.creature_data.items():
            base_name = name.split(' (')[0]
            if base_name not in groups:
                groups[base_name] = []
            groups[base_name].append((copy_id, name))
        
        # Get highest level for each group
        highest_level = {}
        for base_name, creatures in groups.items():
            # Sort by copy_id to get the highest level (assuming higher copy_id = higher level)
            creatures.sort(key=lambda x: x[0])
            highest_copy_id, highest_name = creatures[-1]
            highest_level[highest_copy_id] = highest_name
        
        self.creature_groups = highest_level
        
    def setup_ui(self):
        self.root = tk.Tk()
        self.root.title("Mini World Mod Generator - Desktop Tool")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Generate.TButton', font=('Arial', 10, 'bold'))
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎮 Mini World Mod Generator", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # Form frame
        form_frame = ttk.LabelFrame(main_frame, text="Thông tin Mod", padding="15")
        form_frame.pack(fill=tk.X, pady=(0, 20))
        
        # ID input
        id_frame = ttk.Frame(form_frame)
        id_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(id_frame, text="ID:").pack(side=tk.LEFT)
        self.id_var = tk.StringVar(value="2")
        self.id_entry = ttk.Entry(id_frame, textvariable=self.id_var, width=10)
        self.id_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Author input
        author_frame = ttk.Frame(form_frame)
        author_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(author_frame, text="Tác giả:").pack(side=tk.LEFT)
        self.author_var = tk.StringVar(value="1024277122")
        self.author_entry = ttk.Entry(author_frame, textvariable=self.author_var, width=20)
        self.author_entry.pack(side=tk.LEFT, padx=(10, 0))
        
        # Creature selection
        creature_frame = ttk.Frame(form_frame)
        creature_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(creature_frame, text="Thần thú:").pack(side=tk.LEFT)
        self.creature_var = tk.StringVar()
        self.creature_combo = ttk.Combobox(creature_frame, textvariable=self.creature_var, 
                                          values=list(self.creature_data.values()), 
                                          state="readonly", width=30)
        self.creature_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.creature_combo.bind('<<ComboboxSelected>>', self.on_creature_select)
        
        # Selected creature info
        self.creature_info_label = ttk.Label(form_frame, text="", foreground="blue")
        self.creature_info_label.pack(pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Generate button
        self.generate_btn = ttk.Button(buttons_frame, text="🚀 Tạo Files", 
                                      command=self.generate_files, style='Generate.TButton')
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Auto generate button
        self.auto_btn = ttk.Button(buttons_frame, text="🤖 Auto (Level cao nhất)", 
                                  command=self.auto_generate_all)
        self.auto_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Folder button
        self.folder_btn = ttk.Button(buttons_frame, text="📁 Chọn thư mục", 
                                    command=self.choose_folder)
        self.folder_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Utility buttons frame
        util_frame = ttk.Frame(main_frame)
        util_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Delete button
        self.delete_btn = ttk.Button(util_frame, text="🗑️ Xóa Files Cuối", 
                                    command=self.delete_latest_files, state=tk.DISABLED)
        self.delete_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Reset button
        self.reset_btn = ttk.Button(util_frame, text="🔄 Reset ID", 
                                   command=lambda: self.reset_auto_counters(None))
        self.reset_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status frame
        status_frame = ttk.LabelFrame(main_frame, text="Trạng thái", padding="10")
        status_frame.pack(fill=tk.X)
        
        # Location display
        self.location_label = ttk.Label(status_frame, text=f"📍 Thư mục: {self.folder_path}")
        self.location_label.pack(anchor=tk.W)
        
        # Status display
        self.status_label = ttk.Label(status_frame, text="ℹ️ Trạng thái: Sẵn sàng")
        self.status_label.pack(anchor=tk.W)
        
        # Progress bar
        self.progress = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        # Keyboard shortcuts
        self.root.bind('<Control-z>', self.increment_id_hotkey)
        self.root.bind('<Return>', lambda e: self.generate_files())
        self.auto_btn.bind('<Button-3>', self.reset_auto_counters)
        
        # Set default selection
        if self.creature_data:
            first_creature = list(self.creature_data.values())[0]
            self.creature_combo.set(first_creature)
            self.on_creature_select()
    
    def on_creature_select(self, event=None):
        """Handle creature selection"""
        selected_name = self.creature_var.get()
        if selected_name:
            # Find the copy_id for this creature
            copy_id = None
            for cid, name in self.creature_data.items():
                if name == selected_name:
                    copy_id = cid
                    break
            
            if copy_id:
                self.creature_info_label.config(text=f"Copy ID: {copy_id}")
    
    def get_selected_creature(self):
        """Get the selected creature's copy ID and name"""
        selected_name = self.creature_var.get()
        if selected_name:
            for copy_id, name in self.creature_data.items():
                if name == selected_name:
                    return copy_id, name
        return None, None
    
    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.folder_path)
        if folder:
            self.folder_path = folder
            self.location_label.config(text=f"📍 Thư mục: {folder}")
    
    def generate_files(self):
        copy_id, creature_name = self.get_selected_creature()
        if not copy_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn thần thú")
            return
        
        try:
            id_value = int(self.id_var.get())
            author_value = self.author_var.get().strip()
            
            if not author_value:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên tác giả")
                return
            
            # Start progress
            self.progress.start()
            self.status_label.config(text="⏳ Đang tạo files...")
            
            # Create thread for file generation
            thread = FileGeneratorThread(
                id_value, copy_id, author_value, creature_name, 
                self.auto_result_id_counter, self.on_complete
            )
            thread.start()
            
        except ValueError:
            messagebox.showerror("Lỗi", "ID phải là số nguyên")
    
    def on_complete(self, data):
        """Handle completion of file generation"""
        self.root.after(0, lambda: self.write_files(data))
    
    def write_files(self, data):
        """Write files to disk"""
        try:
            # Stop progress
            self.progress.stop()
            
            # Create files
            files_created = []
            for filename, content in data['files'].items():
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_created.append(file_path)
            
            # Store for deletion
            self.last_generated_files = files_created
            self.delete_btn.config(state=tk.NORMAL)
            
            # Update status
            self.status_label.config(text=f"✅ Đã tạo {len(files_created)} files thành công!")
            
            # Increment ID
            current_id = int(self.id_var.get())
            self.id_var.set(str(current_id + 1))
            
            # Show success message
            messagebox.showinfo("Thành công", 
                               f"Đã tạo {len(files_created)} files cho {data['item_name']}")
            
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="❌ Lỗi khi tạo files")
            messagebox.showerror("Lỗi", f"Không thể tạo files: {str(e)}")
    
    def auto_generate_all(self):
        """Automatically generate files for all creatures at their highest level"""
        if not messagebox.askyesno("Xác nhận", "Tạo files cho tất cả thần thú ở level cao nhất?"):
            return
            
        # Start auto generation in separate thread
        threading.Thread(target=self.auto_generate_worker, daemon=True).start()
    
    def auto_generate_worker(self):
        """Worker thread for auto generation"""
        try:
            author_value = self.author_var.get().strip()
            if not author_value:
                messagebox.showerror("Lỗi", "Vui lòng nhập tên tác giả")
                return
            
            # Update UI
            self.root.after(0, lambda: self.progress.start())
            self.root.after(0, lambda: self.status_label.config(text="⏳ Đang tạo files tự động..."))
            
            current_id = self.auto_id_counter
            files_created = []
            
            for copy_id, creature_name in self.creature_groups.items():
                # Generate files for this creature
                thread = FileGeneratorThread(
                    current_id, copy_id, author_value, creature_name, 
                    self.auto_result_id_counter, self.auto_write_files_callback
                )
                thread.start()
                thread.join()  # Wait for completion
                
                current_id += 1
                
                # Update progress
                self.root.after(0, lambda: self.status_label.config(
                    text=f"⏳ Đang tạo: {creature_name} (ID: {current_id-1})"))
            
            # Update counter
            self.auto_id_counter = current_id
            
            # Complete
            self.root.after(0, lambda: self.auto_complete(
                len(self.creature_groups), len(self.creature_groups)))
            
        except Exception as e:
            self.root.after(0, lambda: self.auto_error(str(e)))
    
    def auto_write_files_callback(self, data):
        """Callback to write files during auto-generation"""
        try:
            files_created = []
            for filename, content in data['files'].items():
                file_path = os.path.join(self.folder_path, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                files_created.append(file_path)
            
            # Add to last generated files
            self.last_generated_files.extend(files_created)
            
        except Exception as e:
            print(f"Error writing files: {e}")
    
    def auto_complete(self, success_count, total_creatures):
        """Handle auto generation completion"""
        self.progress.stop()
        self.delete_btn.config(state=tk.NORMAL)
        self.status_label.config(text=f"✅ Đã tạo {success_count}/{total_creatures} thần thú!")
        messagebox.showinfo("Hoàn thành", f"Đã tạo files cho {success_count} thần thú")
    
    def auto_error(self, error_msg):
        """Handle auto generation error"""
        self.progress.stop()
        self.status_label.config(text="❌ Lỗi khi tạo files tự động")
        messagebox.showerror("Lỗi", f"Lỗi tạo files tự động: {error_msg}")
    
    def reset_auto_counters(self, event):
        """Reset the auto ID and Result ID counters to their default values"""
        self.auto_id_counter = 2
        self.auto_result_id_counter = 4097
        self.status_label.config(text="🔄 Đã reset ID về mặc định")
        messagebox.showinfo("Reset", "Đã reset Auto ID và Result ID về mặc định")
    
    def delete_latest_files(self):
        """Delete files created in the most recent generation"""
        if not self.last_generated_files:
            messagebox.showwarning("Cảnh báo", "Không có files nào để xóa")
            return
        
        if not messagebox.askyesno("Xác nhận", 
                                  f"Xóa {len(self.last_generated_files)} files cuối cùng?"):
            return
        
        try:
            deleted_count = 0
            for file_path in self.last_generated_files:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    deleted_count += 1
            
            self.last_generated_files = []
            self.delete_btn.config(state=tk.DISABLED)
            self.status_label.config(text=f"🗑️ Đã xóa {deleted_count} files")
            messagebox.showinfo("Thành công", f"Đã xóa {deleted_count} files")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa files: {str(e)}")
    
    def increment_id_hotkey(self, event=None):
        """Increments the ID value by 1 when Ctrl+Z is pressed"""
        try:
            current_id = int(self.id_var.get())
            self.id_var.set(str(current_id + 1))
            self.status_label.config(text=f"⬆️ ID tăng thành: {current_id + 1}")
        except ValueError:
            pass
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = CompactModGenerator()
    app.run()