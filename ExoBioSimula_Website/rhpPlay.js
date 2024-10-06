let planetRHPFactors;
let planetName;
let planetType;
let planetErad;

let starRad;
let starName;

let viz;
let planet;
let star;
let temporary_pl;
let starColor;


function estimatePlanetType(density, temp) {
  terrestrial_density_range = [3.0, 6.0];
  super_earth_density_range = [6.1, 11.0];
  ice_density_range = [0.9, 1.9];
  gas_density_range = [0.8, 2.0];
  puffy_gas_density_range = [0.04, 0.79];

  let planet_type = '';

  if (density >= terrestrial_density_range[0] && density <= terrestrial_density_range[1]) {
    if (temp <= 500) {
      planet_type = "Terrestrial";
    } else {
      planet_type = "Unknown";
    } 
  } else if (density >= super_earth_density_range[0] && density <= super_earth_density_range[1]) {
    if (temp <= 500) {
      planet_type = "SuperEarth";
    } else {
      planet_type = "Unknown";
    } 
  } else if (density >= gas_density_range[0] && density <= gas_density_range[1]) {
    planet_type = "Gas";
  } else if (density >= puffy_gas_density_range[0] && density <= puffy_gas_density_range[1]) {
    planet_type = "PuffyGas";
  } else if (density >= ice_density_range[0] && density <= ice_density_range[1]) {
    planet_type = "Ice";
  } else {  
    planet_type = "Unknown";
  }  

  return planet_type;
}


function readCSV(inputStarName, inputPlanetName) {
  var fileName = './data_folder_5/' + inputStarName + '.csv';

  fetch(fileName) 
    .then(response => response.text())
    .then(csvData => {
        const rows = csvData.split('\n').slice(0, -1);
        const headers = rows[0].split(','); // Assuming the first row contains headers
        let planets = {};
        for (let i = 1; i < rows.length; i++) {
          vals = rows[i].split(',');
          console.log(vals)
          planets[vals[0]] = [["Orbital Semi-Major Axis", parseFloat(vals[6])], ["Equilibrium Temp.", parseFloat(vals[11])], ["Gravity", parseFloat(vals[13])], ["Abs. Solar Flux", parseFloat(vals[15])], ["Star Spectral", vals[18]], ["Density", parseFloat(vals[14])], ["Radius", parseFloat(vals[7])]];

          starRad = parseFloat(vals[20]);
        }

        starName = inputStarName;
        planetRHPFactors = planets[inputPlanetName];
        planetName = inputPlanetName;
        planetErad = planetRHPFactors[6][1];

        if (planetRHPFactors[4][1][0] == 'O') {
          starColor = 0x038eeb;
        }
        else if (planetRHPFactors[4][1][0] == 'B') {
          starColor = 0xcaeaf9;
        }
        else if (planetRHPFactors[4][1][0] == 'A') {
          starColor = 0xffffff;
        }
        else if (planetRHPFactors[4][1][0] == 'F') {
          starColor = 0xfcf888;
        }
        else if (planetRHPFactors[4][1][0] == 'G') {
          starColor = 0xfff600;
        }
        else if (planetRHPFactors[4][1][0] == 'K') {
          starColor = 0xff9000;
        }
        else if (planetRHPFactors[4][1][0] == 'M') {
          starColor = 0xff0800;
        }

        setupViz();
        generatePlanet();
    })
    .catch(error => {
        console.error('Error fetching CSV file:', error);
    });
}


function setupViz() {
  viz = new Spacekit.Simulation(document.getElementById('main-container'), {
    jd: 2,
    jdDelta: planetRHPFactors[0][1]*3000,
    camera: {
      initialPosition: [0.04, 0.16, 1.6],
    },
    unitsPerAu: 1.0,
  });

  viz.createStars();
}

function generatePlanet() {
  /*
  viz.createSphere(planetRHPFactors[0], {
    textureUrl: './exo_textures/Terrestrial.jpg',
    debug: {
      showAxes: true,
    },
  });*/
  
  star = viz.createObject(starName, {   //star name
    labelText: starName,
    textureUrl: '{{assets}}/sprites/lensflare0.png',
    position: [0, 0, 0],
    scale: [starRad*60000/215, starRad*60000/215, starRad*60000/215],
    theme: {
      color: starColor
    },
  });
  viz.createAmbientLight();
  viz.createLight([0, 0, 0]);

  planetType = estimatePlanetType(planetRHPFactors[5][1], planetRHPFactors[1][1])


  let texture;
  if (starName == 'Sun') {
    texture = './solar_sys_textures/' + planetName + '.jpg'; 
  }
  else {
    texture = './exo_textures/' + planetType + '.jpg';
  }
  
  temporary_pl = viz.createObject(planetName, {
    labelText: planetName, 
    textureUrl: texture,
    scale: [3000*planetErad*0.0000426, 3000*planetErad*0.0000426, 3000*planetErad*0.0000426],  //from earth radius to au
    ephem: new Spacekit.Ephem( 
      {
        // These parameters define orbit shape.(less than 1)
        a: planetRHPFactors[0][1]*3000,    //radius of (circular)orbit
        e: 0,//parseFloat(plts_orbeccen[index]),
        i: 0,     //inclination(degrees)

        // These parameters define the orientation of the orbit.
        om: 0,     //0 is bottom  //startign point
        w: 0,    //77.0        //startign point as well???
        ma: 0,     //0        //starting poitn again???

        epoch: 0,     //no clue what this does(ignore?)
      },// Need to make habitable zone dynamic
      'deg', //alr so i can run it now?
    ),    //lemme turn off habitable zone
    theme: {
      color: 0xffffff,   //how to determien color of planet based of our dataset?
      orbitColor: 0xff0000
    },
  });
  
  planet = viz.createSphere(planetName + '2', {
    textureUrl: texture,    //change texture dependign on type of planet
    radius: 3000*planetErad * 6371 / 149598000, // in au  
    ephem: temporary_pl._options.ephem,
    levelsOfDetail: [
      { radii: 0, segments: 64 },
      { radii: 30, segments: 16 },
      { radii: 60, segments: 8 },
    ],
    atmosphere: {
      enable: true,
      color: 0xc7c1a8,
    },
    rotation: {
      enable: true,
      speed: 2,
    },
    theme: {
      color: 0xffffff,
      orbitColor: 0xff0000
    }, 
  });

  viz.getViewer().followObject(planet, [-0.75, -0.75, 0.5]);

  //constructHBZone([0, 1]);

}


function alterPlanet(id, val) {
  viz.removeObject(temporary_pl);
  
  switch (id) {
    case "eq_temp":
      alert(val + " K");
      planetRHPFactors[1][1] = val;

      viz.removeObject(planet);
      viz.removeObject(star);
      generatePlanet();
      break;
      
    case "abs_solar_flux":
      alert(val);
      planetRHPFactors[3][1] = val;
      break;
      
    case "st_type":
      types = ["O","B","A","F","G","K","M"];
      alert(types[Math.abs(6-val)] + " type");

      planetRHPFactors[4][1][0] = types[Math.abs(6-val)];
  
      if (planetRHPFactors[4][1][0] == 'O') {
        starColor = 0x038eeb;
      }
      else if (planetRHPFactors[4][1][0] == 'B') {
        starColor = 0xcaeaf9;
      }
      else if (planetRHPFactors[4][1][0] == 'A') {
        starColor = 0xffffff;
      }
      else if (planetRHPFactors[4][1][0] == 'F') {
        starColor = 0xfcf888;
      }
      else if (planetRHPFactors[4][1][0] == 'G') {
        starColor = 0xfff600;
      }
      else if (planetRHPFactors[4][1][0] == 'K') {
        starColor = 0xff9000;
      }
      else if (planetRHPFactors[4][1][0] == 'M') {
        starColor = 0xff0800;
      }

      viz.removeObject(planet);
      viz.removeObject(star);
      generatePlanet();
      
      break;

    case "pl_orbsmaxm":
      alert(val + " au");
      planetRHPFactors[0][1] = val;

      viz.removeObject(planet);
      viz.removeObject(star);
      generatePlanet();
      
      break;
  }

  
}