const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('file-input');

// Kliklenende faýl saýlaýan penjiräni açmak
dropZone.addEventListener('click', () => fileInput.click());

// Surat süýräp üstüne getirilende stili üýtgetmek
dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => {
        dropZone.classList.remove('drag-over');
    });
});

// Surat taşlanylanda faýly kabul etmek
dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    if (e.dataTransfer.files.length) {
        fileInput.files = e.dataTransfer.files;
        updateDropZoneText(e.dataTransfer.files[0].name);
    }
});

// Adaty saýlanylanda hem adyny görkezmek
fileInput.addEventListener('change', () => {
    if (fileInput.files.length) {
        updateDropZoneText(fileInput.files[0].name);
    }
});

function updateDropZoneText(fileName) {
    const textElement = dropZone.querySelector('.drop-text');
    const iconElement = dropZone.querySelector('.upload-icon');
    
    iconElement.style.color = '#10b981';
    iconElement.className = 'fa-solid fa-circle-check upload-icon';
    textElement.innerHTML = `Saýlanan faýl: <br><strong style="color: #fff;">${fileName}</strong>`;
}

// Form ugradylanda Loader-i görkezmek
const uploadForm = document.getElementById('upload-form');
const loaderWrapper = document.getElementById('loader-wrapper');

if (uploadForm) {
    uploadForm.addEventListener('submit', () => {
        loaderWrapper.style.display = 'flex';
    });
}

// Kamera Elementlerini we Öňki Elementleri Tapýarys
const startCameraBtn = document.getElementById('start-camera-btn');
const captureBtn = document.getElementById('capture-btn');
const webcam = document.getElementById('webcam');
const canvas = document.getElementById('photo-canvas');
const videoContainer = document.getElementById('video-container');
const cameraFeedback = document.getElementById('camera-feedback');

let stream = null;

// 1. Kamerany Işletmek
startCameraBtn.addEventListener('click', async () => {
    try {
        // Telefonyň yzky kamerasyny (environment) açmaga çalyşýarys, eger ýok bolsa öňkisini açar
        stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: "environment" }, 
            audio: false 
        });
        webcam.srcObject = stream;
        videoContainer.style.display = 'block';
        captureBtn.style.display = 'flex';
        startCameraBtn.innerHTML = '<i class="fa-solid fa-rotate"></i> Kamerany Ýap / Täzele';
        
        // Eger surat öň düşürilen bolsa resetleýäris
        webcam.style.display = 'block';
        canvas.style.display = 'none';
        cameraFeedback.style.display = 'none';
    } catch (err) {
        alert("Kamera açylmady! Rugsat berilmändir ýa-da kamera tapylmady: " + err);
    }
});

// 2. Surata Düşürmek (Capture)
captureBtn.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    
    // Canvas-yň ölçeglerini wideonyň ölçegine düzýäris
    canvas.width = webcam.videoWidth;
    canvas.height = webcam.videoHeight;
    
    // Wideodaky kadry canvas-a çyzýarys
    context.drawImage(webcam, 0, 0, canvas.width, canvas.height);
    
    // Wizual effektler
    webcam.style.display = 'none';
    canvas.style.display = 'block';
    cameraFeedback.style.display = 'block';
    
    // 3. Canvas-daky suraty Django Formasyna Geçirmek (Blob arkaly)
    canvas.toBlob((blob) => {
        // Täze faýl döredýäris
        const file = new File([blob], "camera_capture.jpg", { type: "image/jpeg" });
        
        // Django-nyň öňki file-input elementini tapyp, suraty içine salýarys
        const fileInput = document.getElementById('file-input');
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
        
        // Öňki drop-zone tekstini hem täzeleýäris, ulanyjy biler ýaly
        updateDropZoneText("Kameradan düşürilen surat taýyn!");
    }, 'image/jpeg', 0.95);
});