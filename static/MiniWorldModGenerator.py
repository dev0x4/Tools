#!/usr/bin/env python3
"""
Mini World Mod Generator Desktop Application
Standalone version for download

Hướng dẫn sử dụng:
1. Cài đặt Python 3.7+ trên máy tính
2. Cài đặt thư viện tkinter: pip install tkinter (thường có sẵn với Python)
3. Chạy file này: python MiniWorldModGenerator.py
4. Sử dụng giao diện để tạo mod files

Features:
- Giao diện đồ họa thân thiện
- Tự động tạo mod files theo định dạng Mini World
- Hỗ trợ tất cả creatures và items
- Tự động tạo folder structure
- Export ZIP files
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json
import os
import tempfile
import zipfile
import datetime
import uuid
import random
import string
import shutil

class FileGeneratorThread(threading.Thread):
    def __init__(self, id_value, copyid_value, author_value, item_name, start_result_id, callback):
        super().__init__()
        self.id_value = id_value
        self.copyid_value = copyid_value
        self.author_value = author_value
        self.item_name = item_name
        self.start_result_id = start_result_id
        self.callback = callback
        
    def run(self):
        try:
            # Generate mod files content
            data = self.generate_mod_files()
            self.callback(data)
        except Exception as e:
            self.callback({'error': str(e)})
    
    def generate_mod_files(self):
        """Generate all mod files"""
        files = {}
        
        # Generate random values for mod
        mod_uuid = str(uuid.uuid4())
        version = f"1.0.{random.randint(1, 999)}"
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Actor file
        actor_content = {
            "PhysicsActor": {
                f"{self.copyid_value}": {
                    "CopyId": self.copyid_value,
                    "Foreign": f"{self.copyid_value}du",
                    "Id": self.id_value
                }
            }
        }
        files[f"{self.copyid_value}du.json"] = {
            'content': json.dumps(actor_content, indent=2, ensure_ascii=False),
            'type': 'actor'
        }
        
        # Horse/Ride file
        horse_content = {
            "HorseRide": {
                f"{self.copyid_value}": self.copyid_value
            }
        }
        files[f"{self.copyid_value}duride.json"] = {
            'content': json.dumps(horse_content, indent=2, ensure_ascii=False),
            'type': 'horse'
        }
        
        # Crafting file
        craft_content = {
            "Recipes": [
                {
                    "foreign": f"craft{self.copyid_value}",
                    "results": [
                        {
                            "foreign": f"item{self.copyid_value}",
                            "id": self.start_result_id
                        }
                    ],
                    "components": [
                        {
                            "foreign": "stone",
                            "id": 1,
                            "amount": 1
                        }
                    ],
                    "id": self.id_value,
                    "unlock_level": 1,
                    "priority": 1,
                    "type": 0,
                    "tab": 3,
                    "amount": 1
                }
            ]
        }
        files[f"craft{self.copyid_value}.json"] = {
            'content': json.dumps(craft_content, indent=2, ensure_ascii=False),
            'type': 'crafting'
        }
        
        # Item file
        item_content = {
            "Items": [
                {
                    "foreign": f"item{self.copyid_value}",
                    "id": self.start_result_id,
                    "name": self.item_name,
                    "icon": f"ui_item_{self.copyid_value}",
                    "mesh": f"mesh_{self.copyid_value}",
                    "type": 1,
                    "sub_type": 1,
                    "stack_size": 64,
                    "durability": 100,
                    "use_action": {
                        "type": "spawn_actor",
                        "actor_id": self.copyid_value
                    },
                    "rarity": 1,
                    "description": f"Mod item created by {self.author_value}"
                }
            ],
            "ModInfo": {
                "author": self.author_value,
                "filename": f"miniworld_mod_{self.author_value}_{timestamp}.zip",
                "uuid": mod_uuid,
                "version": version,
                "created_date": timestamp,
                "properties": {
                    "copyid": self.copyid_value,
                    "id": self.id_value,
                    "result_id": self.start_result_id
                },
                "ai_settings": {
                    "friendly": True,
                    "aggressive": False,
                    "neutral": True
                }
            }
        }
        files[f"item{self.copyid_value}.json"] = {
            'content': json.dumps(item_content, indent=2, ensure_ascii=False),
            'type': 'item'
        }
        
        return {
            'files': files,
            'metadata': {
                'author_value': self.author_value,
                'copyid_value': self.copyid_value,
                'id_value': self.id_value,
                'item_name': self.item_name,
                'timestamp': timestamp,
                'zip_filename': f"miniworld_mod_{self.author_value}_{timestamp}.zip"
            }
        }

class CompactModGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Mini World Mod Generator v2.0")
        self.root.geometry("800x600")
        
        # Auto counters
        self.auto_id_counter = 2
        self.auto_result_id_counter = 4097
        self.last_generated_files = []
        
        # Output folder
        self.output_folder = os.path.expanduser("~/Desktop")
        
        # Load creature data
        self.load_creature_data()
        self.group_creatures_by_level()
        
        # Setup UI
        self.setup_ui()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-z>', self.increment_id_hotkey)

    def load_creature_data(self):
        """Load creature data from the provided list"""
        # Your creature data here - same as in the web version
        creature_text = """4534|Slime lvl 1
4535|Slime lvl 2
4536|Slime lvl 3
4538|Golem lvl 1
4539|Golem lvl 2
4540|Golem lvl 3
4541|Wizard lvl 1
4542|Wizard lvl 2
4543|Wizard lvl 3
4544|Archer lvl 1
4545|Archer lvl 2
4546|Archer lvl 3
4547|Knight lvl 1
4548|Knight lvl 2
4549|Knight lvl 3
4550|Dragon lvl 1
4551|Dragon lvl 2
4552|Dragon lvl 3"""
        
        self.creature_data = {}
        for line in creature_text.strip().split('\n'):
            if '|' in line:
                copyid, name = line.split('|')
                self.creature_data[int(copyid)] = name

    def group_creatures_by_level(self):
        """Group creatures by their base name and return the highest level for each"""
        base_creatures = {}
        
        for copyid, name in self.creature_data.items():
            # Extract base name (remove level info)
            base_name = name.split(' lvl')[0]
            
            if base_name not in base_creatures:
                base_creatures[base_name] = []
            
            base_creatures[base_name].append((copyid, name))
        
        # Get highest level for each creature type
        self.creature_groups = {}
        for base_name, creatures in base_creatures.items():
            # Sort by level (highest first)
            creatures.sort(key=lambda x: x[1], reverse=True)
            highest_level = creatures[0]
            self.creature_groups[highest_level[0]] = highest_level[1]

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Mini World Mod Generator", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # ID field
        ttk.Label(main_frame, text="ID:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.id_var = tk.StringVar(value="3")
        id_entry = ttk.Entry(main_frame, textvariable=self.id_var, width=20)
        id_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Creature selection
        ttk.Label(main_frame, text="Creature:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.creature_var = tk.StringVar()
        creature_combo = ttk.Combobox(main_frame, textvariable=self.creature_var, width=40)
        creature_combo['values'] = [f"{copyid} - {name}" for copyid, name in self.creature_groups.items()]
        creature_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        creature_combo.bind('<<ComboboxSelected>>', self.on_creature_select)
        
        # Author field
        ttk.Label(main_frame, text="Author:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.author_var = tk.StringVar(value="ModCreator")
        author_entry = ttk.Entry(main_frame, textvariable=self.author_var, width=20)
        author_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Output folder
        ttk.Label(main_frame, text="Output Folder:").grid(row=4, column=0, sticky=tk.W, pady=5)
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        
        self.folder_var = tk.StringVar(value=self.output_folder)
        folder_entry = ttk.Entry(folder_frame, textvariable=self.folder_var, width=30)
        folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        folder_btn = ttk.Button(folder_frame, text="Browse", command=self.choose_folder)
        folder_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Generate button
        generate_btn = ttk.Button(btn_frame, text="Generate Files", command=self.generate_files)
        generate_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Auto generate button
        auto_btn = ttk.Button(btn_frame, text="Auto Generate All", command=self.auto_generate_all)
        auto_btn.grid(row=0, column=1, padx=(0, 10))
        auto_btn.bind('<Button-3>', self.reset_auto_counters)  # Right click
        
        # Delete latest files button
        delete_btn = ttk.Button(btn_frame, text="Delete Latest Files", command=self.delete_latest_files)
        delete_btn.grid(row=0, column=2)
        
        # Status text
        self.status_text = tk.Text(main_frame, height=15, width=70)
        self.status_text.grid(row=6, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar for status text
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.status_text.yview)
        scrollbar.grid(row=6, column=2, sticky=(tk.N, tk.S))
        self.status_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        folder_frame.columnconfigure(0, weight=1)

    def on_creature_select(self, event=None):
        """Handle creature selection"""
        selected = self.creature_var.get()
        if selected and ' - ' in selected:
            copyid = selected.split(' - ')[0]
            name = selected.split(' - ')[1]
            self.status_text.insert(tk.END, f"Selected: {name} (ID: {copyid})\n")
            self.status_text.see(tk.END)

    def get_selected_creature(self):
        """Get the selected creature's copy ID and name"""
        selected = self.creature_var.get()
        if selected and ' - ' in selected:
            copyid = int(selected.split(' - ')[0])
            name = selected.split(' - ')[1]
            return copyid, name
        return None, None

    def choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.output_folder)
        if folder:
            self.output_folder = folder
            self.folder_var.set(folder)

    def generate_files(self):
        """Generate mod files"""
        try:
            # Validate inputs
            id_value = int(self.id_var.get())
            copyid_value, item_name = self.get_selected_creature()
            author_value = self.author_var.get().strip()
            
            if not copyid_value:
                messagebox.showerror("Error", "Please select a creature")
                return
            
            if not author_value:
                messagebox.showerror("Error", "Please enter author name")
                return
            
            self.status_text.insert(tk.END, f"Generating files for {item_name}...\n")
            self.status_text.see(tk.END)
            
            # Start generation in thread
            thread = FileGeneratorThread(
                id_value, copyid_value, author_value, item_name,
                self.auto_result_id_counter, self.on_complete
            )
            thread.start()
            
        except ValueError:
            messagebox.showerror("Error", "ID must be a number")
        except Exception as e:
            messagebox.showerror("Error", f"Error generating files: {str(e)}")

    def on_complete(self, data):
        """Handle completion of file generation"""
        if 'error' in data:
            messagebox.showerror("Error", data['error'])
            return
        
        self.write_files(data)

    def write_files(self, data):
        """Write files to disk"""
        try:
            timestamp = data['metadata']['timestamp']
            author = data['metadata']['author_value']
            
            # Create output directory
            output_dir = os.path.join(self.output_folder, f"miniworld_mod_{author}_{timestamp}")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create folder structure
            folders = {
                'actor': 'Actor',
                'horse': 'Horse',
                'crafting': 'Crafting', 
                'item': 'Item'
            }
            
            for folder_name in folders.values():
                os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)
            
            # Write files
            written_files = []
            for filename, file_data in data['files'].items():
                content = file_data['content']
                file_type = file_data['type']
                
                # Determine target folder
                target_folder = folders.get(file_type, '')
                file_path = os.path.join(output_dir, target_folder, filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                written_files.append(file_path)
                self.status_text.insert(tk.END, f"Created: {file_path}\n")
            
            # Create ZIP file
            zip_path = f"{output_dir}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in written_files:
                    relative_path = os.path.relpath(file_path, output_dir)
                    zipf.write(file_path, relative_path)
            
            # Store for deletion
            self.last_generated_files = [output_dir, zip_path]
            
            self.status_text.insert(tk.END, f"ZIP created: {zip_path}\n")
            self.status_text.insert(tk.END, "Generation completed!\n\n")
            self.status_text.see(tk.END)
            
            messagebox.showinfo("Success", f"Files generated successfully!\nLocation: {output_dir}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error writing files: {str(e)}")

    def auto_generate_all(self):
        """Automatically generate files for all creatures at their highest level"""
        if not self.author_var.get().strip():
            messagebox.showerror("Error", "Please enter author name for auto generation")
            return
        
        self.status_text.insert(tk.END, "Starting auto generation for all creatures...\n")
        self.status_text.see(tk.END)
        
        # Start auto generation in thread
        thread = threading.Thread(target=self.auto_generate_worker)
        thread.start()

    def auto_generate_worker(self):
        """Worker thread for auto generation"""
        try:
            author_value = self.author_var.get().strip()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Create main output directory
            output_dir = os.path.join(self.output_folder, f"miniworld_auto_mod_{author_value}_{timestamp}")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create folder structure
            folders = {
                'actor': 'Actor',
                'horse': 'Horse',
                'crafting': 'Crafting',
                'item': 'Item'
            }
            
            for folder_name in folders.values():
                os.makedirs(os.path.join(output_dir, folder_name), exist_ok=True)
            
            total_creatures = len(self.creature_groups)
            success_count = 0
            all_written_files = []
            
            current_id = self.auto_id_counter
            current_result_id = self.auto_result_id_counter
            
            for copyid, name in self.creature_groups.items():
                try:
                    # Generate files for this creature
                    thread = FileGeneratorThread(
                        current_id, copyid, author_value, name,
                        current_result_id, self.auto_write_files_callback
                    )
                    thread.run()  # Run synchronously
                    
                    success_count += 1
                    current_id += 1
                    current_result_id += 1
                    
                    # Update counters
                    self.auto_id_counter = current_id
                    self.auto_result_id_counter = current_result_id
                    
                    self.status_text.insert(tk.END, f"Generated: {name} ({success_count}/{total_creatures})\n")
                    self.status_text.see(tk.END)
                    
                except Exception as e:
                    self.status_text.insert(tk.END, f"Error generating {name}: {str(e)}\n")
                    self.status_text.see(tk.END)
            
            # Create final ZIP
            zip_path = f"{output_dir}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(output_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        relative_path = os.path.relpath(file_path, output_dir)
                        zipf.write(file_path, relative_path)
            
            # Store for deletion
            self.last_generated_files = [output_dir, zip_path]
            
            self.auto_complete(success_count, total_creatures)
            
        except Exception as e:
            self.auto_error(str(e))

    def auto_write_files_callback(self, data):
        """Callback to write files during auto-generation"""
        if 'error' in data:
            return
        
        try:
            timestamp = data['metadata']['timestamp']
            author = data['metadata']['author_value']
            
            # Use the existing auto generation directory
            output_dir = os.path.join(self.output_folder, f"miniworld_auto_mod_{author}_{timestamp}")
            
            # Create folder structure if needed
            folders = {
                'actor': 'Actor',
                'horse': 'Horse', 
                'crafting': 'Crafting',
                'item': 'Item'
            }
            
            # Write files
            for filename, file_data in data['files'].items():
                content = file_data['content']
                file_type = file_data['type']
                
                # Determine target folder
                target_folder = folders.get(file_type, '')
                file_path = os.path.join(output_dir, target_folder, filename)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
        except Exception as e:
            self.status_text.insert(tk.END, f"Error writing auto files: {str(e)}\n")

    def auto_complete(self, success_count, total_creatures):
        """Handle auto generation completion"""
        self.status_text.insert(tk.END, f"Auto generation completed! {success_count}/{total_creatures} creatures processed.\n")
        self.status_text.insert(tk.END, f"New counters - ID: {self.auto_id_counter}, Result ID: {self.auto_result_id_counter}\n\n")
        self.status_text.see(tk.END)
        
        messagebox.showinfo("Auto Generation Complete", 
                           f"Successfully generated files for {success_count} out of {total_creatures} creatures!")

    def auto_error(self, error_msg):
        """Handle auto generation error"""
        self.status_text.insert(tk.END, f"Auto generation error: {error_msg}\n\n")
        self.status_text.see(tk.END)
        messagebox.showerror("Auto Generation Error", error_msg)

    def reset_auto_counters(self, event):
        """Reset the auto ID and Result ID counters to their default values"""
        self.auto_id_counter = 2
        self.auto_result_id_counter = 4097
        self.status_text.insert(tk.END, "Reset counters to default values (ID: 2, Result ID: 4097)\n")
        self.status_text.see(tk.END)
        messagebox.showinfo("Reset Complete", "ID and Result ID counters have been reset to default values.")

    def delete_latest_files(self):
        """Delete files created in the most recent generation"""
        if not self.last_generated_files:
            messagebox.showinfo("Info", "No files to delete")
            return
        
        deleted_count = 0
        for file_path in self.last_generated_files:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    deleted_count += 1
                    self.status_text.insert(tk.END, f"Deleted: {file_path}\n")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    deleted_count += 1
                    self.status_text.insert(tk.END, f"Deleted folder: {file_path}\n")
            except Exception as e:
                self.status_text.insert(tk.END, f"Error deleting {file_path}: {str(e)}\n")
        
        self.last_generated_files = []
        self.status_text.insert(tk.END, f"Deleted {deleted_count} items\n\n")
        self.status_text.see(tk.END)
        
        if deleted_count > 0:
            messagebox.showinfo("Delete Complete", f"Deleted {deleted_count} items")

    def increment_id_hotkey(self, event=None):
        """Increments the ID value by 1 when Ctrl+Z is pressed"""
        try:
            current_id = int(self.id_var.get())
            self.id_var.set(str(current_id + 1))
            self.status_text.insert(tk.END, f"ID incremented to {current_id + 1}\n")
            self.status_text.see(tk.END)
        except ValueError:
            pass

    def run(self):
        """Start the application"""
        self.status_text.insert(tk.END, "Mini World Mod Generator Ready!\n")
        self.status_text.insert(tk.END, "Keyboard shortcuts: Ctrl+Z = Increment ID\n")
        self.status_text.insert(tk.END, "Right-click 'Auto Generate All' to reset counters\n\n")
        self.root.mainloop()

if __name__ == "__main__":
    app = CompactModGenerator()
    app.run()