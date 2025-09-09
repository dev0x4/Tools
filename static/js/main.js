// Main JavaScript for Mini World Mod Generator
document.addEventListener('DOMContentLoaded', function() {
    // Initialize components
    initializeFormHandlers();
    initializeCreatureSelection();
    initializeModals();
    initializeButtons();
    initializeKeyboardShortcuts();
    initializeDesktopDownload();
    
    // Global variables
    let lastGeneratedFiles = [];
    let autoIdCounter = 2;
    let autoResultIdCounter = 4097;
    
    // Form handling
    function initializeFormHandlers() {
        const form = document.getElementById('modGeneratorForm');
        const generateBtn = document.getElementById('generateBtn');
        const progressModal = new bootstrap.Modal(document.getElementById('progressModal'));
        const successModal = new bootstrap.Modal(document.getElementById('successModal'));
        
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Validate form
            if (!validateForm()) {
                return;
            }
            
            // Show loading state
            showLoadingState(generateBtn);
            progressModal.show();
            
            // Submit form data
            const formData = new FormData(form);
            
            fetch('/generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                progressModal.hide();
                hideLoadingState(generateBtn);
                
                if (data.success) {
                    showSuccessModal(data, successModal);
                    // Enable delete button for last generated files
                    document.getElementById('deleteBtn').disabled = false;
                    updateStatus('✅ Tạo files thành công!', 'success');
                } else {
                    showErrorMessage(data.error || 'Đã xảy ra lỗi khi tạo file mod');
                }
            })
            .catch(error => {
                progressModal.hide();
                hideLoadingState(generateBtn);
                showErrorMessage('Lỗi mạng: ' + error.message);
            });
        });
    }
    
    // Creature selection handling
    function initializeCreatureSelection() {
        const creatureSelect = document.getElementById('creature_select');
        const creatureInfo = document.getElementById('creature_info');
        const creatureDetails = document.getElementById('creature_details');
        
        if (!creatureSelect) return;
        
        creatureSelect.addEventListener('change', function() {
            const selectedValue = this.value;
            const selectedText = this.options[this.selectedIndex].text;
            
            if (selectedValue) {
                // Show creature info
                if (creatureInfo) {
                    creatureInfo.style.display = 'block';
                    
                    // Extract copy ID and name
                    const [copyId, name] = selectedText.split(' - ');
                    
                    if (creatureDetails) {
                        creatureDetails.innerHTML = `
                            <strong>Copy ID:</strong> ${copyId}<br>
                            <strong>Tên Item:</strong> ${name}
                        `;
                    }
                }
                
                // Update status
                updateStatus(`Đã chọn: ${selectedText}`, 'info');
            } else {
                if (creatureInfo) {
                    creatureInfo.style.display = 'none';
                }
                if (creatureDetails) {
                    creatureDetails.innerHTML = '';
                }
                updateStatus('Sẵn sàng', 'success');
            }
        });
        
        // Initialize with default selection
        if (creatureSelect.value) {
            creatureSelect.dispatchEvent(new Event('change'));
        }
    }
    
    // Modal initialization
    function initializeModals() {
        // Close modals when clicking outside
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('modal')) {
                const modal = bootstrap.Modal.getInstance(e.target);
                if (modal) {
                    modal.hide();
                }
            }
        });
    }
    
    // Initialize button handlers
    function initializeButtons() {
        // Auto button
        const autoBtn = document.getElementById('autoBtn');
        const progressModal = new bootstrap.Modal(document.getElementById('progressModal'));
        const successModal = new bootstrap.Modal(document.getElementById('successModal'));
        
        autoBtn.addEventListener('click', function() {
            if (!confirm('Bạn có muốn tạo files cho tất cả thần thú (level cao nhất) không?\n' + 
                        'Điều này sẽ tạo một file ZIP với tất cả các mod chỉ cho thần thú level cao nhất.')) {
                return;
            }
            
            const authorValue = document.getElementById('author_value').value.trim();
            if (!authorValue) {
                showErrorMessage('Tên tác giả là bắt buộc');
                return;
            }
            
            // Show loading state
            autoBtn.disabled = true;
            autoBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>⏳ Đang tạo...';
            progressModal.show();
            updateStatus('Đang tạo auto mod...', 'warning');
            
            // Submit auto generate request
            const formData = new FormData();
            formData.append('author_value', authorValue);
            
            fetch('/auto_generate', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                progressModal.hide();
                autoBtn.disabled = false;
                autoBtn.innerHTML = '<i class="fas fa-robot me-1"></i>🤖 Auto';
                
                if (data.success) {
                    showAutoSuccessModal(data, successModal);
                    updateStatus(`✅ Tạo thành công ${data.total_files} files cho ${data.total_creatures} thần thú!`, 'success');
                } else {
                    showErrorMessage(data.error || 'Đã xảy ra lỗi khi tạo auto mod');
                }
            })
            .catch(error => {
                progressModal.hide();
                autoBtn.disabled = false;
                autoBtn.innerHTML = '<i class="fas fa-robot me-1"></i>🤖 Auto';
                showErrorMessage('Lỗi mạng: ' + error.message);
            });
        });
        
        // Delete button
        const deleteBtn = document.getElementById('deleteBtn');
        deleteBtn.addEventListener('click', function() {
            if (!confirm('Bạn có chắc chắn muốn xóa các file đã tạo cuối cùng không?')) {
                return;
            }
            
            // For now, just show a message since we don't track individual files in web version
            showErrorMessage('Chức năng xóa file chưa khả dụng trong phiên bản web');
        });
        
        // Reset button
        const resetBtn = document.getElementById('resetBtn');
        resetBtn.addEventListener('click', function() {
            if (!confirm('Bạn có chắc chắn muốn reset ID về giá trị mặc định không?\n' + 
                        'ID mặc định: 2\nResult ID mặc định: 4097')) {
                return;
            }
            
            fetch('/reset_counters', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    autoIdCounter = data.auto_id_counter;
                    autoResultIdCounter = data.auto_result_id_counter;
                    updateStatus('✅ Đã reset ID về mặc định', 'success');
                } else {
                    showErrorMessage(data.error || 'Lỗi khi reset ID');
                }
            })
            .catch(error => {
                showErrorMessage('Lỗi mạng: ' + error.message);
            });
        });
        
        // Folder button (placeholder)
        const folderBtn = document.getElementById('folderBtn');
        folderBtn.addEventListener('click', function() {
            updateStatus('📁 Thư mục: Desktop (mặc định)', 'info');
        });
    }
    
    // Initialize keyboard shortcuts
    function initializeKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + Z to increment ID
            if ((e.ctrlKey || e.metaKey) && e.key === 'z') {
                e.preventDefault();
                incrementId();
            }
            
            // Ctrl/Cmd + Enter to generate
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('generateBtn').click();
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                });
            }
        });
    }
    
    // Increment ID function
    function incrementId() {
        const idInput = document.getElementById('id_value');
        const currentId = parseInt(idInput.value) || 0;
        const newId = currentId + 1;
        idInput.value = newId;
        updateStatus(`ID đã tăng lên: ${newId}`, 'info');
    }
    
    // Form validation
    function validateForm() {
        const authorName = document.getElementById('author_value').value.trim();
        const creatureSelect = document.getElementById('creature_select').value;
        const idValue = document.getElementById('id_value').value;
        
        // Check required fields
        if (!authorName) {
            showErrorMessage('Tên tác giả là bắt buộc');
            document.getElementById('author_value').focus();
            return false;
        }
        
        if (!creatureSelect) {
            showErrorMessage('Chọn thần thú là bắt buộc');
            document.getElementById('creature_select').focus();
            return false;
        }
        
        if (!idValue || parseInt(idValue) <= 0) {
            showErrorMessage('ID phải là số dương');
            document.getElementById('id_value').focus();
            return false;
        }
        
        return true;
    }
    
    // Loading state management
    function showLoadingState(button) {
        const btnText = button.querySelector('.btn-text');
        const btnLoading = button.querySelector('.btn-loading');
        
        btnText.classList.add('d-none');
        btnLoading.classList.remove('d-none');
        button.disabled = true;
    }
    
    function hideLoadingState(button) {
        const btnText = button.querySelector('.btn-text');
        const btnLoading = button.querySelector('.btn-loading');
        
        btnText.classList.remove('d-none');
        btnLoading.classList.add('d-none');
        button.disabled = false;
    }
    
    // Success modal display
    function showSuccessModal(data, modal) {
        const filesList = document.getElementById('filesList');
        const downloadBtn = document.getElementById('downloadBtn');
        
        // Display generated files with preview and individual download options
        filesList.innerHTML = `
            <div class="alert alert-info">
                <h6><i class="fas fa-file-code me-2"></i>Files đã tạo:</h6>
                <div class="row">
                    ${data.file_details.map(file => `
                        <div class="col-md-6 mb-2">
                            <div class="card">
                                <div class="card-body p-2">
                                    <h6 class="card-title mb-1">${file.name}</h6>
                                    <p class="card-text mb-1">
                                        <small class="text-muted">
                                            Loại: ${file.type} | Kích thước: ${file.size} bytes
                                        </small>
                                    </p>
                                    <div class="btn-group btn-group-sm">
                                        <button class="btn btn-outline-primary" onclick="previewFile('${data.session_key}', '${file.name}')">
                                            <i class="fas fa-eye"></i> Xem
                                        </button>
                                        <button class="btn btn-outline-success" onclick="downloadSingleFile('${data.session_key}', '${file.name}')">
                                            <i class="fas fa-download"></i> Tải
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        // Store session key for later use
        window.currentSessionKey = data.session_key;
        
        // Show modal
        modal.show();
        
        // Handle download button click
        downloadBtn.onclick = function(e) {
            e.preventDefault();
            
            // Create a temporary link for download
            const link = document.createElement('a');
            link.href = data.download_zip_url || data.download_url;
            link.download = data.metadata.zip_filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Close modal after download
            setTimeout(() => {
                modal.hide();
            }, 1000);
        };
    }
    
    // Auto success modal display
    function showAutoSuccessModal(data, modal) {
        const filesList = document.getElementById('filesList');
        const downloadBtn = document.getElementById('downloadBtn');
        
        // Display auto generation results
        filesList.innerHTML = `
            <div class="alert alert-success">
                <h6><i class="fas fa-robot me-2"></i>Auto Generation hoàn thành!</h6>
                <p class="mb-1"><strong>Tổng số thần thú:</strong> ${data.total_creatures}</p>
                <p class="mb-1"><strong>Tổng số files:</strong> ${data.total_files}</p>
                <p class="mb-1"><strong>Cấu trúc thư mục:</strong> Actor, Horse, Crafting, Item</p>
                <p class="mb-0"><strong>File ZIP:</strong> ${data.filename}</p>
            </div>
        `;
        
        // Set download link
        downloadBtn.href = data.download_url;
        downloadBtn.download = data.filename;
        
        // Store session key for later use
        window.currentSessionKey = data.session_key;
        
        // Show modal
        modal.show();
        
        // Handle download button click
        downloadBtn.onclick = function(e) {
            e.preventDefault();
            
            // Create a temporary link for download
            const link = document.createElement('a');
            link.href = data.download_url;
            link.download = data.filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // Close modal after download
            setTimeout(() => {
                modal.hide();
            }, 1000);
        };
    }
    
    // Update status function
    function updateStatus(message, type = 'info') {
        const statusDisplay = document.getElementById('status_display');
        if (!statusDisplay) return;
        
        const colorClass = {
            'success': 'text-success',
            'error': 'text-danger',
            'warning': 'text-warning',
            'info': 'text-info'
        };
        
        statusDisplay.innerHTML = `<span class="${colorClass[type] || 'text-info'}">${message}</span>`;
    }
    
    // Global functions for file preview and download
    window.previewFile = function(sessionKey, filename) {
        fetch(`/preview/${sessionKey}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const file = data.files.find(f => f.name === filename);
                    if (file) {
                        showFilePreview(file);
                    }
                } else {
                    showErrorMessage('Không thể tải file để xem trước');
                }
            })
            .catch(error => {
                showErrorMessage('Lỗi khi tải file: ' + error.message);
            });
    };
    
    window.downloadSingleFile = function(sessionKey, filename) {
        const url = `/download_single/${sessionKey}/${encodeURIComponent(filename)}`;
        window.location.href = url;
    };
    
    // Show file preview modal
    function showFilePreview(file) {
        // Create preview modal if not exists
        let previewModal = document.getElementById('previewModal');
        if (!previewModal) {
            previewModal = document.createElement('div');
            previewModal.className = 'modal fade';
            previewModal.id = 'previewModal';
            previewModal.innerHTML = `
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">
                                <i class="fas fa-file-code me-2"></i>Xem trước file
                            </h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div id="previewContent"></div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Đóng</button>
                            <button type="button" class="btn btn-primary" id="downloadPreviewBtn">
                                <i class="fas fa-download me-1"></i>Tải về
                            </button>
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(previewModal);
        }
        
        // Update preview content
        const previewContent = document.getElementById('previewContent');
        previewContent.innerHTML = `
            <div class="mb-3">
                <h6><i class="fas fa-info-circle me-1"></i>Thông tin file:</h6>
                <ul class="list-unstyled">
                    <li><strong>Tên:</strong> ${file.name}</li>
                    <li><strong>Loại:</strong> ${file.type}</li>
                    <li><strong>Kích thước:</strong> ${file.size} bytes</li>
                </ul>
            </div>
            <div class="mb-3">
                <h6><i class="fas fa-code me-1"></i>Nội dung:</h6>
                <pre class="bg-light p-3 rounded" style="max-height: 400px; overflow-y: auto;"><code>${file.full_content}</code></pre>
            </div>
        `;
        
        // Set download handler
        const downloadBtn = document.getElementById('downloadPreviewBtn');
        downloadBtn.onclick = function() {
            window.downloadSingleFile(window.currentSessionKey, file.name);
        };
        
        // Show modal
        const modal = new bootstrap.Modal(previewModal);
        modal.show();
    }
    
    // Error message display
    function showErrorMessage(message) {
        // Create alert element
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            <i class="fas fa-exclamation-triangle me-2"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Insert at top of container
        const container = document.querySelector('.container');
        container.insertBefore(alert, container.firstChild);
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
        
        // Scroll to top to show error
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
    
    // Desktop download functionality
    function initializeDesktopDownload() {
        const downloadDesktopBtn = document.getElementById('downloadDesktopBtn');
        const downloadDesktopBtn2 = document.getElementById('downloadDesktopBtn2');
        
        function handleDesktopDownload(event) {
            event.preventDefault();
            
            // Create download link
            const downloadLink = document.createElement('a');
            downloadLink.href = '/download_desktop';
            downloadLink.download = 'MiniWorldModGenerator.exe';
            
            // Add to DOM, click, and remove
            document.body.appendChild(downloadLink);
            downloadLink.click();
            document.body.removeChild(downloadLink);
            
            // Show success message
            updateStatus('✅ Đang tải Desktop Tool...', 'success');
        }
        
        if (downloadDesktopBtn) {
            downloadDesktopBtn.addEventListener('click', handleDesktopDownload);
        }
        
        if (downloadDesktopBtn2) {
            downloadDesktopBtn2.addEventListener('click', handleDesktopDownload);
        }
    }

    // Utility functions
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Form auto-save (optional)
    function initializeAutoSave() {
        const form = document.getElementById('modGeneratorForm');
        const inputs = form.querySelectorAll('input[type="text"], input[type="number"]');
        
        inputs.forEach(input => {
            const saveKey = `miniworld_mod_${input.name}`;
            
            // Load saved value
            const savedValue = localStorage.getItem(saveKey);
            if (savedValue && !input.value) {
                input.value = savedValue;
            }
            
            // Save on change
            input.addEventListener('input', debounce(() => {
                localStorage.setItem(saveKey, input.value);
            }, 500));
        });
    }
    
    // Initialize auto-save
    initializeAutoSave();
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to generate
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            document.getElementById('generateBtn').click();
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modals = document.querySelectorAll('.modal.show');
            modals.forEach(modal => {
                const modalInstance = bootstrap.Modal.getInstance(modal);
                if (modalInstance) {
                    modalInstance.hide();
                }
            });
        }
    });
    
    // Responsive adjustments
    function handleResize() {
        const creatureGrid = document.querySelector('.creature-grid');
        if (creatureGrid) {
            if (window.innerWidth < 768) {
                creatureGrid.style.maxHeight = '300px';
            } else {
                creatureGrid.style.maxHeight = '400px';
            }
        }
    }
    
    window.addEventListener('resize', debounce(handleResize, 250));
    handleResize(); // Initial call
    
    // Service worker registration (for PWA capabilities)
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/sw.js').catch(err => {
            console.log('Service Worker registration failed:', err);
        });
    }
    
    // Add visual feedback for form interactions
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href && href !== '#' && href.startsWith('#')) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });
});

// Global error handler
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    // You could send this to a logging service
});

// Unhandled promise rejection handler
window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // You could send this to a logging service
});
