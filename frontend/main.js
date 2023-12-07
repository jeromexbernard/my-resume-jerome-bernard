window.addEventListener('DOMContentLoaded', (event)=> {
    getVisitorCount();
    updateVisitorCount();
});

 async function updateVisitorCount() {

    try{
        const response = await fetch ('http://localhost:7071/api/GetResumeCounter', {method: 'POST'});
        const data = await response.json();
        
        var countValue = data.count;
        
        document.getElementById('getcounter').textContent = countValue;
        //console.log("This is data",data);
        return data;
    }
    catch(error){
        console.error('Error from getVistorCounterFunc', error);
    } 

}

async function getVisitorCount() {

    try{
        const response = await fetch ('http://localhost:7071/api/GetResumeCounter', {method: 'GET'});
        const data = await response.json();
        var countValue = data.count;
        
        document.getElementById('getcounter').textContent = countValue;
        //console.log("This is data",data);
        return data;
    }
    catch(error){
        console.error('Error from getVistorCounterFunc', error);
    }

   

}

