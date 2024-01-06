// webcam_app/static/webcam_app/js/webcam.js
document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('snap');

    navigator.mediaDevices.getUserMedia({ video: true })
        .then((stream) => {
            video.srcObject = stream;
        })
        .catch((error) => {
            console.error('Error accessing webcam:', error);
        });

    captureButton.addEventListener('click', function () {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

        const imageData = canvas.toDataURL('image/png');

        $.ajax({
            url: '/capture_image/',
            method: 'POST',
            data: { image_data: imageData },
            success: function () {
                console.log('Image captured and saved!');
            },
            error: function (error) {
                console.error('Error capturing image:', error);
            }
        });
    });
});
