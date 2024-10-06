function makeRanks() {
  fetch('/data_folder_5/sorted_data_nasa.csv') 
    .then(response => response.text())
    .then(csvData => {
        const rows = csvData.split('\n');
        //const headers = rows[0].split(','); // Assuming the first row contains headers

        let names_RHP = []
        for (let i = 1; i < rows.length; i++) {
          vals = rows[i].split(',')
          names_RHP.push([vals[0], String(parseFloat(vals[1]).toFixed(2)) + ' RHP'])
        }
        
        document.querySelector('.podium-first .winner-name').textContent = names_RHP[0][0];
        document.querySelector('.podium-first .RHP_podium').textContent = names_RHP[0][1];
      
        document.querySelector('.podium-second .winner-name').textContent = names_RHP[1][0];
        document.querySelector('.podium-second .RHP_podium').textContent = names_RHP[1][1];

        document.querySelector('.podium-third .winner-name').textContent = names_RHP[2][0];
        document.querySelector('.podium-third .RHP_podium').textContent = names_RHP[2][1];
        
    })
    .catch(error => {
        console.error('Error fetching CSV file:', error);
    });
}


function populateLeaderboard() {
  fetch('/data_folder_5/sorted_data_nasa.csv') 
  .then(response => response.text())
  .then(csvData => {
      const rows = csvData.split('\n');
      let avgRHP = 0;
      let medianRHP = 0;
      
      for (let i = 1; i < rows.length; i++) {
        vals = rows[i].split(',');

        if (parseFloat(vals[1]).toFixed(2) == "NaN") continue;
        
        let name_RHP = [vals[0], String(parseFloat(vals[1]).toFixed(2)) + ' RHP'];
        avgRHP += parseFloat(parseFloat(vals[1]).toFixed(2));
        
        let tr = document.createElement("tr");
        
        let td1 = document.createElement("td");
        td1.class = 'number';
        td1.textContent = i;
        td1.style.width = '1rem';
        td1.style.fontSize = '2.2rem';
        td1.style.fontWeight = 'bold';
        td1.style.textAlign = 'left';
        
        let td2 = document.createElement("td");
        td2.class = 'name';
        td2.textContent = name_RHP[0];
        td2.style.textAlign = 'left';
        td2.style.fontSize = '1.2rem';
        
        let td3 = document.createElement("td");
        td3.class = 'points';
        td3.textContent = name_RHP[1];
        td3.style.fontWeight = 'bold';
        td3.style.fontSize = '1.3rem';
        td3.style.display = 'flex';
        td3.style.justifyContent = 'flex-end';
        td3.style.alignItems = 'center';


        tr.appendChild(td1);
        tr.appendChild(td2);
        tr.appendChild(td3);
        document.querySelector('#ldbrd-table').appendChild(tr);
      }

    avgRHP = avgRHP / (rows.length - 1);
    medianRHP = rows[Math.floor(rows.length / 2)].split(",")[1];
    
    console.log(avgRHP)
    console.log(medianRHP);
  })
  .catch(error => {
      console.error('Error fetching CSV file:', error);
  });
}