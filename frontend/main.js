window.addEventListener('DOMContentLoaded', (event)=> {
    getVisitorCount();
    updateVisitorCount();
});

 async function updateVisitorCount() {

    try{
        const response = await fetch ('https://getresumecounterjb.azurewebsites.net/api/http_trigger?code=6gtrd74yTvMFaeaEBGdQpf-l62RcY2TZEH7N4xUsZ7gAAzFu_GFgVA==', {method: 'POST'});
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
        const response = await fetch ('https://getresumecounterjb.azurewebsites.net/api/http_trigger?code=6gtrd74yTvMFaeaEBGdQpf-l62RcY2TZEH7N4xUsZ7gAAzFu_GFgVA==', {method: 'GET'});
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

