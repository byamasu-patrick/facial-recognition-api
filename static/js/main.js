window.onload = () => {
    const progress = document.querySelector(".progress");
    const uploadButton = document.getElementById("submit");
    const divUpload = document.getElementById("block-content");
    const inputFile = document.getElementById("audioupload");
    const alert = document.getElementById("alert-2");

    inputFile.addEventListener('change', () => {
        var file = inputFile.value.split("\\");
        var fileName = file[file.length - 1];
        document.getElementById("file_name").innerHTML = fileName;
    });

    uploadButton.addEventListener('click', (event) => {
       
        if(inputFile.value == ""){
            event.preventDefault();
            alert.style.display="flex";
            document.getElementById("message").innerHTML = "No file has been selected yet, please select a file"
            setTimeout(() => {
                alert.style.display="none";
            }, 3000);
            
        }
        else{
            divUpload.style.visibility="visible";
            setTimeout(() => {
                progress.style.width="25%";
                setTimeout(() => {
                    progress.style.width="45%";
                    setTimeout(() => {
                        progress.style.width="60%";
                        setTimeout(() => {
                            progress.style.width="75%";
                            setTimeout(() => {
                                progress.style.width="95%";
                            }, 1500);
                        }, 1500);               
                    }, 1500);  
                }, 1500);
                          
            }, 2000);  

        }
        

    });

    // progress.style.width="80%";


}