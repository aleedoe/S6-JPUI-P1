const API_BASE_URL = 'http://localhost:5000'; // Sesuaikan dengan URL backend Flask Anda

// Fungsi untuk berpindah tab
function openTab(evt, tabName) {
    const tabcontents = document.getElementsByClassName("tabcontent");
    for (let i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = "none";
    }
    
    const tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// Preview foto saat dipilih (untuk registrasi)
document.getElementById('studentPhotos').addEventListener('change', function(e) {
    const preview = document.getElementById('photoPreview');
    preview.innerHTML = '';
    
    for (let i = 0; i < e.target.files.length; i++) {
        const file = e.target.files[i];
        const reader = new FileReader();
        
        reader.onload = function(event) {
            const img = document.createElement('img');
            img.src = event.target.result;
            img.style.maxWidth = '100px';
            img.style.maxHeight = '100px';
            img.style.margin = '5px';
            preview.appendChild(img);
        };
        
        reader.readAsDataURL(file);
    }
});

// Preview foto presensi
document.getElementById('attendancePhoto').addEventListener('change', function(e) {
    const preview = document.getElementById('attendancePreview');
    
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        const reader = new FileReader();
        
        reader.onload = function(event) {
            preview.src = event.target.result;
            preview.style.display = 'block';
        };
        
        reader.readAsDataURL(file);
    } else {
        preview.style.display = 'none';
    }
});

// Fungsi registrasi siswa
async function registerStudent() {
    const name = document.getElementById('studentName').value;
    const nis = document.getElementById('studentNIS').value;
    const classId = document.getElementById('studentClass').value;
    const photosInput = document.getElementById('studentPhotos');
    
    if (!name || !nis || !classId || photosInput.files.length < 3) {
        alert('Harap isi semua field dan unggah minimal 3 foto');
        return;
    }
    
    const formData = new FormData();
    formData.append('name', name);
    formData.append('nis', nis);
    formData.append('class_id', classId);
    
    for (let i = 0; i < photosInput.files.length; i++) {
        formData.append('photos', photosInput.files[i]);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/student/register`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            document.getElementById('registerResult').innerHTML = `
                <p style="color: green;">Registrasi berhasil!</p>
                <p>ID Siswa: ${result.student_id}</p>
                <p>Nama: ${name}</p>
                <p>NIS: ${nis}</p>
                <p>Kelas: ${classId}</p>
            `;
            
            // Reset form
            document.getElementById('studentName').value = '';
            document.getElementById('studentNIS').value = '';
            document.getElementById('studentClass').value = '';
            document.getElementById('studentPhotos').value = '';
            document.getElementById('photoPreview').innerHTML = '';
        } else {
            document.getElementById('registerResult').innerHTML = `
                <p style="color: red;">Error: ${result.error || 'Gagal mendaftarkan siswa'}</p>
            `;
        }
    } catch (error) {
        document.getElementById('registerResult').innerHTML = `
            <p style="color: red;">Error: ${error.message}</p>
        `;
    }
}

// Fungsi presensi harian
async function takeAttendance() {
    const classId = document.getElementById('attendanceClass').value;
    const photoInput = document.getElementById('attendancePhoto');
    
    if (!classId || photoInput.files.length === 0) {
        alert('Harap pilih kelas dan unggah foto presensi');
        return;
    }
    
    const formData = new FormData();
    formData.append('class_id', classId);
    formData.append('photo', photoInput.files[0]);
    
    try {
        const response = await fetch(`${API_BASE_URL}/attendance/take-attendance`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (response.ok) {
            document.getElementById('attendanceResult').innerHTML = `
                <p style="color: green;">Presensi berhasil!</p>
                <p>Siswa: ${result.student.name} (NIS: ${result.student.nis})</p>
                <p>Status: Hadir</p>
                <img src="${API_BASE_URL}/${result.photo_url}" style="max-width: 300px; margin-top: 10px;">
            `;
        } else {
            document.getElementById('attendanceResult').innerHTML = `
                <p style="color: red;">${result.error || 'Gagal mengambil presensi'}</p>
            `;
        }
    } catch (error) {
        document.getElementById('attendanceResult').innerHTML = `
            <p style="color: red;">Error: ${error.message}</p>
        `;
    }
}

// Fungsi cek riwayat presensi
async function getAttendanceHistory() {
    const studentId = document.getElementById('historyStudentID').value;
    
    if (!studentId) {
        alert('Harap masukkan ID Siswa');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}/attendance/${studentId}`);
        const result = await response.json();
        
        if (response.ok) {
            let html = `<h3>Riwayat Presensi</h3>`;
            
            if (result.length > 0) {
                html += `<table border="1" cellpadding="5" cellspacing="0">
                    <tr>
                        <th>Tanggal</th>
                        <th>Status</th>
                        <th>Foto</th>
                    </tr>`;
                
                result.forEach(attendance => {
                    const date = new Date(attendance.created_at).toLocaleString();
                    html += `
                    <tr>
                        <td>${date}</td>
                        <td>${attendance.status}</td>
                        <td><img src="${API_BASE_URL}/${attendance.photo_url}" style="max-width: 100px;"></td>
                    </tr>`;
                });
                
                html += `</table>`;
            } else {
                html += `<p>Tidak ada riwayat presensi untuk siswa ini</p>`;
            }
            
            document.getElementById('historyResult').innerHTML = html;
        } else {
            document.getElementById('historyResult').innerHTML = `
                <p style="color: red;">${result.error || 'Gagal mengambil riwayat presensi'}</p>
            `;
        }
    } catch (error) {
        document.getElementById('historyResult').innerHTML = `
            <p style="color: red;">Error: ${error.message}</p>
        `;
    }
}