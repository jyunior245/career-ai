// File input handler
const fileInput = document.getElementById('resumeFile');
const fileInfo = document.getElementById('fileInfo');
const jobTextarea = document.getElementById('jobDescription');
const jobCounter = document.getElementById('jobCounter');
const submitBtn = document.getElementById('submitBtn');
const form = document.getElementById('analysisForm');

// Handle file selection
if (fileInput) {
    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            const fileSizeMB = (file.size / (1024 * 1024)).toFixed(2);
            const fileName = file.name.toLowerCase();
            
            fileInfo.textContent = `${file.name} (${fileSizeMB}MB)`;
            fileInput.classList.remove('is-invalid');
            
            // Check file type
            if (!fileName.endsWith('.pdf')) {
                fileInput.classList.add('is-invalid');
                fileInfo.textContent += ' - ❌ O arquivo deve ser um PDF';
                return;
            }
            
            // Check file size
            if (file.size > 10 * 1024 * 1024) {
                fileInput.classList.add('is-invalid');
                fileInfo.textContent += ' - ⚠️ O arquivo excede o limite de 10MB';
            } else {
                fileInput.classList.remove('is-invalid');
            }
        } else {
            fileInfo.textContent = 'Nenhum arquivo selecionado';
            fileInput.classList.remove('is-invalid');
        }
    });
}

// Update job description character count
if (jobTextarea) {
    jobTextarea.addEventListener('input', () => {
        const count = jobTextarea.value.length;
        const maxCount = 10000;
        jobCounter.textContent = `${count} / ${maxCount} caracteres`;
        
        if (count > maxCount) {
            jobTextarea.classList.add('is-invalid');
        } else {
            jobTextarea.classList.remove('is-invalid');
        }
    });
}

// Form submission handler
if (form) {
    form.addEventListener('submit', (e) => {
        const hasFile = fileInput.files.length > 0;
        const jobLength = jobTextarea.value.length;
        
        if (!hasFile) {
            e.preventDefault();
            alert('Por favor selecione um arquivo PDF.');
            return;
        }
        
        // Check file type
        const fileName = fileInput.files[0].name.toLowerCase();
        if (!fileName.endsWith('.pdf')) {
            e.preventDefault();
            alert('O arquivo deve ser um PDF. Selecione um arquivo PDF válido.');
            return;
        }
        
        // Check file size
        if (fileInput.files[0].size > 10 * 1024 * 1024) {
            e.preventDefault();
            alert('O arquivo excede o limite de 10MB. Escolha um arquivo menor.');
            return;
        }
        
        if (jobLength > 10000) {
            e.preventDefault();
            alert('Por favor, assegure que a descrição da vaga tenha no máximo 10.000 caracteres.');
            return;
        }
        
        if (jobLength < 50) {
            e.preventDefault();
            alert('Por favor, assegure que a descrição da vaga tenha pelo menos 50 caracteres.');
            return;
        }
        
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner"></span> Analyzing...';
    });
}

// Dismiss alerts after 5 seconds
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 300);
    }, 5000);
});
