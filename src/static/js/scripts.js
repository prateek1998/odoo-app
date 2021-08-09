function showAlert(){
    const steps = [1, 2, 3, 4, 5, 6, 7]
    const swalQueue = Swal.mixin({
        progressSteps: steps,
        onBeforeOpen: () => {
            Swal.showLoading()
        }
    })
    swalQueue.fire({
        title: 'Please Wait !', 
        html: 'data uploading', 
        allowOutsideClick: false,
        timer: 1000,
        currentProgressStep: 0 
    })
    .then(function(){ 
        swalQueue.fire({
            title: 'Please Wait !', 
            html: 'Creating Telnet Socket',
            allowOutsideClick: false,  
            timer: 1000,
            currentProgressStep: 1
        })
        .then(function() {
            swalQueue.fire({
                title: 'Please Wait !', 
                html: 'Configuring User and Password',
                allowOutsideClick: false,  
                timer: 8000,
                currentProgressStep: 2
            })
            .then(function() {
                swalQueue.fire({
                    title: 'Please Wait !', 
                    html: 'Configuring Management IP',
                    allowOutsideClick: false,  
                    timer: 5000,
                    currentProgressStep: 3
                })
                .then(function() {
                    swalQueue.fire({
                        title: 'Please Wait !', 
                        html: 'Configuring SSH and creating SSH Connection',
                        allowOutsideClick: false,  
                        timer: 2000,
                        currentProgressStep: 4
                    })
                    .then(function() {
                        swalQueue.fire({
                            title: 'Please Wait !', 
                            html: 'Firmware Upgrading ',
                            allowOutsideClick: false,  
                            timer: 50000,
                            currentProgressStep: 5
                        })  
                        .then(function() {
                            swalQueue.fire({
                                title: 'Please Wait !', 
                                html: 'Copying Primary flash to Secondary flash',
                                allowOutsideClick: false,  
                                timer: 30000,
                                currentProgressStep: 6
                            })
                            .then(function() {
                                swalQueue.fire({
                                    title: 'Please Wait !', 
                                    html: 'Performing Rebooting Switch',
                                    allowOutsideClick: false,  
                                    timer: 30000,
                                    currentProgressStep: 7
                                })
                            })  
                        })  
                    })  
                })
            })
        })
    })    
}

window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

});
