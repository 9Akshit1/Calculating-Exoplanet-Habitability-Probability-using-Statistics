let starName = '';
let star_spect = '';
let plts_names = [];
let plts_orbper = [];
let plts_orbsmax = [];
let plts_Erad = []; 
let plts_Emass = []; 
let plts_orbeccen = [];
let plts_insol = [];
let plts_eq_temp = []; 
let plts_density = [];
let plts_gravity = []; 
let plts_albedo = [];
let plts_types = [];
let plts_abs_solar_flux = [];
let plts_probabilities = [];
let plts_disc_year = [];
let sy_snum = 0;
let sy_pnum = 0;
let st_teff = 0;
let st_rad = 0;
let st_mass = 0;
let st_met = 0;
let st_metratio = '';
let st_log_gravity = 0;
let HB_r_i = 0;
let HB_r_o = 0;
let sy_dist = 0;
let sy_vmag = 0;
let star_color = '';

let planets = [];
let star = 0;
let starTexture = '';
let HBParticles = [[], []];

let name_btnArray = [];
let HBPlaneMode = true;
let HBSphereMode = true;
let viz;


function alterHBPlaneMode() {
  HBPlaneMode = !HBPlaneMode;  

  if (HBPlaneMode) {
    document.getElementById("HB-plane-mode").innerHTML = "Turn Off Habitable Plane";

    constructHBZone([0]);

  } else {
    document.getElementById("HB-plane-mode").innerHTML = "Turn On Habitable Plane";

    HBParticles[0].forEach(particle => {
      viz.removeObject(particle);
    });

    HBParticles[0] = [];
  }
}

function alterHBSphereMode() {
    HBSphereMode = !HBSphereMode;  

  if (HBSphereMode) {
    document.getElementById("HB-sphere-mode").innerHTML = "Turn Off Habitable Sphere";

    constructHBZone([1]);

  } else {
    document.getElementById("HB-sphere-mode").innerHTML = "Turn On Habitable Sphere";

    HBParticles[1].forEach(particle => {
      viz.removeObject(particle);
    });

    HBParticles[1] = [];
  }
}


function estimatePlanetType(density, temp, Emass) {
  terrestrial_density_range = [3.0, 6.0];
  super_earth_density_range = [6.1, 11.0];
  ice_density_range = [0.9, 1.9];
  gas_density_range = [0.8, 2.0];
  puffy_gas_density_range = [0.04, 0.79];

  planet_type = "";

  if (density >= terrestrial_density_range[0] && density <= terrestrial_density_range[1]) {
    if (Emass >= 400) {
      planet_type = "Gas";
    }
    if (temp <= 500) {
      planet_type = "Terrestrial";
    } else {
      planet_type = "Unknown";
    } 
  } else if (density >= super_earth_density_range[0] && density <= super_earth_density_range[1]) {
    if (Emass >= 400) {
      planet_type = "Gas";
    }
    planet_type = "SuperEarth";
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


function readCSV(inputStarName) {
  var fileName = './data_folder_5/' + inputStarName + '.csv';
  
  fetch(fileName) 
    .then(response => response.text())
    .then(csvData => {
        const rows = csvData.split('\n').slice(0, -1);
        const headers = rows[0].split(','); // Assuming the first row contains headers

        let names = []
        for (let i = 1; i < rows.length; i++) {
          vals = rows[i].split(',')
          names.push(vals[0])
          if (i == rows.length - 1){
            names.push(vals[1])    //star name
          }
        }

        const thead = document.querySelector('#planet_names thead tr');
        
        names.forEach(name => {
            const name_btn = document.createElement('button');
            name_btn.textContent = name.trim(); // Trim any leading/trailing whitespace

            var text = name.trim();

            name_btn.setAttribute('id', text);
            name_btn.setAttribute('class', 'name_btn');
            name_btnArray.push(name_btn);

            thead.appendChild(name_btn);
        }); 
      
        const buttons = document.querySelectorAll('name_btn');

        buttons.forEach(button => {
          button.addEventListener('click', () => {
            buttons.forEach(button => button.classList.remove('active'));
            button.classList.add('active');
            });
        });
        // Populate table headers
        //const thead = document.querySelector('#planet_names thead tr');
      /*
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header.trim(); // Trim any leading/trailing whitespace
            thead.appendChild(th);
        }); */
        
  
        // Populate table rows
        const tbody = document.querySelector('#planet_names tbody');
        for (let i = 1; i < rows.length; i++) {
            const rowData = rows[i].split(',');
          
            const tr = document.createElement('tr');
            rowData.forEach((data, index) => {
                const td = document.createElement('td');
                td.textContent = data.trim();
                //var text = data.trim();

              /*
                if (index == 0) {
                  td.setAttribute('id', text);
                  tdArray.push(td);
                } */
              
                tr.appendChild(td);
            });
            
            
            if (i == 1) {    
              starName = rowData[1]
              sy_snum = rowData[2]
              sy_pnum = rowData[3]
              star_spect = rowData[18]
              star_color = 0

              if (star_spect[0] == 'O') {
                star_color = 0x038eeb //Blue
                starTexture = './star_textures/' + 'blue_star.png';
              }
              else if (star_spect[0] == 'B') {
                star_color = 0xcaeaf9  //blue-white
                starTexture = './star_textures/' + 'blue-white_star.png';
              }
              else if (star_spect[0] == 'A') {
                star_color = 0xffffff       //white
                starTexture = './star_textures/' + 'white_star.png';
              }
              else if (star_spect[0] == 'F') {
                star_color = 0xfcf888         //white-yellow
                starTexture = './star_textures/' + 'yellow-white_star.png';
              }
              else if (star_spect[0] == 'G') {
                star_color = 0xfff600           //yellow
                starTexture = './star_textures/' + 'yellow_star.png';
              }
              else if (star_spect[0] == 'K') {
                star_color = 0xff9000           //orange
                starTexture = './star_textures/' + 'orange_star.jpg';   //original image hwich is why thsi is jpg
              }
              else if (star_spect[0] == 'M') {
                star_color = 0xff0800          //red
                starTexture = './star_textures/' + 'red_star.png';
              }

              st_teff = rowData[19]
              st_rad = rowData[20]
              st_mass = rowData[21]
              st_met = rowData[22]
              st_metratio = rowData[23]
              st_log_gravity = rowData[24]
              HB_r_i = rowData[25]
              HB_r_o = rowData[26]
              console.log(rowData)
              sy_dist = rowData[27]
              sy_vmag = rowData[28]
            }
            plts_names.push(rowData[0]) 
            plts_disc_year.push(rowData[4])
            plts_orbper.push(rowData[5])
            plts_orbsmax.push(rowData[6])
            plts_Erad.push(rowData[7])
            plts_Emass.push(rowData[8])
            plts_orbeccen.push(rowData[9])
            plts_insol.push(rowData[10])
            plts_eq_temp.push(rowData[11])
            plts_density.push(rowData[12])
        plts_types.push(estimatePlanetType(parseFloat(rowData[14]), parseFloat(rowData[11]), parseFloat(rowData[8])));
            plts_gravity.push(rowData[13])
            plts_albedo.push(rowData[14])
            plts_abs_solar_flux.push(rowData[15])
            plts_probabilities.push(rowData[29]) 
            //tbody.appendChild(tr);
        }
        
        generate_system()
    })
    .catch(error => {
        console.error('Error fetching CSV file:', error);
    });
}

function calculateInclination(orbitalPeriod, semiMajorAxis, planet, pl_mass) {
  m = pl_mass
  T = orbitalPeriod
  a = semiMajorAxis
  //Given the orbital period (T) and the eccentricity (e) of the orbit, we can relate the angular velocity (w) to the orbital parameters using Kepler's laws or orbital mechanics equations.
  //Assuming a circular orbit for simplicity, the angular velocity (w) can be calculated as:
  w = 2 * Math.PI / T
  //Then, the time derivative of the azimuthal angle (ϕ) can be expressed as equal:
  azi_ang = w
  //Given the Cartesian coordinates (x,y,z), polar angle(θ) can be calculated using trigonometric functions. Here's how to calculate it
  var now = new Date();
  var julianDate = (now / 86400000) - (now.getTimezoneOffset() / 1440) + 2440587.5;
  xyz = planet.getPosition(julianDate)
  console.log('xyz:', xyz)
  r = Math.sqrt(xyz[0]**2 + xyz[1]**2 + xyz[2]**2)
  polar_ang = Math.acos(xyz[2] / r);
  //So, pϕ is the coefficient of the ^ϕ unit vector in the momentum vector. Therefore pϕ is:
  p = m * r * Math.sin(polar_ang) * azi_ang
  Lz = r * p
  //Using Kepler's third law, we can relate the orbital period (T) and semi-major axis (a) and solve for orbtial velocity:
  v = 2 * Math.PI * a / T
  L = m * v * a
  //Since Lz is equal to L times cos(inclination), we can rearrange for inclination:
  console.log('Lz/L:', Lz/L) 
  ratio = Lz/L
  
  if (ratio > 1) {
    ratio = 1
  }
  else if (ratio < -1) {
  ratio = -1
  }
  inclination = Math.acos(ratio)
  console.log('inclination:', inclination)
  return inclination
}

function generate_system() {
  viz = new Spacekit.Simulation(document.getElementById('main-UI'), {
    jd: 0,
    jdDelta: parseFloat(plts_orbsmax[0]),
    camera: {
      initialPosition: [0.04, 0.16, 1.6],
    },
    unitsPerAu: 1.0,
  }); 

  for (let i = 0; i < name_btnArray.length; i++) {
    name_btn = name_btnArray[i]
    name_btn.addEventListener('click', function() {
      if (i != name_btnArray.length - 1) {
        PlanetFunction(viz, i);
      }
      else {
        StarFunction(viz);
      }
    });
  }
  document.getElementById('HB-plane-mode').addEventListener('click', function() {
    alterHBPlaneMode();
  });
  document.getElementById('HB-sphere-mode').addEventListener('click', function() {
    alterHBSphereMode();
  });
  
  // Create a starry background using Yale Bright Star Catalog Data.
  viz.createStars();
  
  // Create our first object - the star - using a preset space object.
  star = viz.createObject(starName, {   //star name
    labelText: starName,
    textureUrl: '{{assets}}/sprites/lensflare0.png',
    position: [0, 0, 0],
    scale: [parseFloat(st_rad)*20/215, parseFloat(st_rad)*20/215, parseFloat(st_rad)*20/215],  //from sun radius to au, multiplying radius by 8 to account for the corona reach
    theme: {
      color: star_color
    },
  });
  viz.createAmbientLight();
  viz.createLight([1, 1, 1]);
  var temporary_pl = 0
  
  plts_names.forEach((e, index) => {
    let texture;
    if (starName == 'Sun') {
      texture = './solar_sys_textures/' + plts_names[index] + '.jpg'; 
    }
    else {
      texture = './exo_textures/' + plts_types[index] + '.jpg';
    }
    temporary_pl = viz.createObject(plts_names[index], {
      labelText: plts_names[index], 
      textureUrl: texture,
      scale: [parseFloat(plts_Erad)*0.0000426, parseFloat(plts_Erad)*0.0000426, parseFloat(plts_Erad)*0.0000426],  //from earth radius to au
      ephem: new Spacekit.Ephem( 
        {
          // These parameters define orbit shape.(less than 1)
          a: parseFloat(plts_orbsmax[index]),    //in terms of star_diameter    //radius of (circular)orbit
          e: parseFloat(plts_orbeccen[index]),     //makes it oval/egg (eliptical)(less than 1)
          i: 0,     //inclination(degrees)
          
          // These parameters define the orientation of the orbit.
          om: 0,     //0 is bottom  
          w: 0,    //77.0      
          ma: 0,     //0       
          
          epoch: 0,     
        },
        'deg',
      ),    
      theme: {
        color: 0x000000,   
        orbitColor: 0xff0000
      },
    });
    temporary_pl._options.ephem.attrs.i = calculateInclination(parseFloat(plts_orbper[index]), parseFloat(plts_orbsmax[index]), temporary_pl, parseFloat(plts_Emass[index]) * 5.9722 * 10**24)  
    planets.push(temporary_pl);
  });

  constructHBZone([0, 1]);
  
}


function constructHBZone(fields) {
  const surfaceParticlesCount = 10;
  const nearParticlesCount = surfaceParticlesCount * 25000;
  const particleSize = 3;
  
  fields.forEach(e => {
    let nearPositions = [];
    let color = 0x0492c2;

    if (e == 1) color = 0x26ff26;
    
    fillParticles(nearParticlesCount, parseFloat(HB_r_i), parseFloat(HB_r_o), nearPositions, e+2);   //in terms of star_diameter
    HBParticles[e].push(viz.createStaticParticles('near', nearPositions, {
      defaultColor: color,
      size: particleSize, 
    })
    );
  });
}


function fillParticles(count, minRange, maxRange, particles, D) {
  for (let i = 0; i < count; i++) {
    const newParticle = randomPosition(minRange, maxRange, D);
    particles.push(newParticle);
  }
}

function randomPosition(minRange, maxRange, D) {
  const delta = maxRange - minRange;
  let mag = 1;
  
  if (delta > 0) {
    mag = delta * Math.random() + minRange;
  }

  const ra = randomAngle(0, 2 * Math.PI);
  const dec = randomAngle(-Math.PI/2, Math.PI/2);

  var z = 0;
  var x = HB_r_o  * Math.cos(dec) * Math.cos(ra);
  var y = HB_r_o  * Math.cos(dec) * Math.sin(ra);
  
  if (D == 3) {
    z = HB_r_o  * Math.sin(dec);
  } 
  
  if (x**2 + y**2 <= HB_r_i**2) return [100,100,100];
  
  return [x, y, z];
} 

function randomAngle(min, max) {
  const delta = max - min;
  return min + Math.random() * delta;
} 

function PlanetFunction(viz, pl_index) {
  let texture = '';
  
  if (starName == 'Sun') {
    texture = './solar_sys_textures/' + plts_names[pl_index] + '.jpg'; 
  }
  else {
    texture = './exo_textures/' + plts_types[pl_index] + '.jpg';
  } 
  
  const planet = viz.createSphere(plts_names[pl_index] + '2', {
    textureUrl: texture,    //change texture dependign on type of planet
    radius: parseFloat(plts_Erad[pl_index]) * 6371 / 149598000, // in au  
    ephem: planets[pl_index]._options.ephem,
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
      enable: true,          //only if planet is nto tidally locked
      speed: 2,
    },
    theme: {
      orbitColor: 0xff0000
    }, 
  });
  viz.createLight([5, 5, 5]);

  if (plts_names[pl_index] == "Saturn") {
    planet.addRings(74270.580913, 140478.924731, './saturn_rings_top.png');
  }

  viz.getViewer().followObject(planet, [-0.75, -0.75, 0.5]);
  
  // Get all div elements with class 'value'
  var titleDivs = document.querySelectorAll('.title');
  var valueDivs = document.querySelectorAll('.value');

  // Values to assign to each div
  var titles = ['NAME', 'DISC YEAR', "ORBITAL PERIOD", 'SEMI-MAJOR AXIS', 'RADIUS(Earth)', 'MASS(Earth)', 'ECCENTRICITY', 'INSOLATION FLUX(Earth)', 'EQUILIBRIUM TEMP.', 'DENSITY', 'GRAVITY', 'ALBEDO', 'ABS. SOLAR FLUX.', 'RHP PROBABILTIY']
  var values = [plts_names[pl_index], plts_disc_year[pl_index], plts_orbper[pl_index], plts_orbsmax[pl_index], plts_Erad[pl_index], plts_Emass[pl_index], plts_orbeccen[pl_index], plts_insol[pl_index], plts_eq_temp[pl_index], plts_density[pl_index], plts_gravity[pl_index], plts_albedo[pl_index], String(parseFloat(plts_abs_solar_flux[pl_index]))  + '%', String(plts_probabilities[pl_index]) + '%'];

  // Assign values to each div
  valueDivs.forEach(function(div, index) {
    div.innerHTML = values[index];
  });
  titleDivs.forEach(function(div, index) {
    div.innerHTML = titles[index];
  }); 

  //for stop follow object
  stop_follow_btn = document.getElementById('stop-follow')
  stop_follow_btn.addEventListener('click', function() {
    viz.getViewer().stopFollowingObject()
    viz.getViewer().cameraControls.target.set(0,0,0);
  });
}

function StarFunction(viz) {
 const exo_star = viz.createSphere(starName + '2', {
    textureUrl: starTexture,    //change texture dependign on type of star
    radius: parseFloat(st_rad) * 1/215,  
    ephem: star._options.ephem,
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
      enable: true,          //only if planet is nto tidally locked
      speed: 2,
    },
  });
  viz.createLight([5, 5, 5]);

  viz.getViewer().followObject(exo_star, [-0.75, -0.75, 0.5]);

  // Get all div elements with class 'value' adn 'title'
  var titleDivs = document.querySelectorAll('.title');
  var valueDivs = document.querySelectorAll('.value');
  console.log(valueDivs)

  // Values to assign to each div
  var titles = ['NAME', 'SPECTRAL TYPE', "EFFECTIVE TEMP.", 'RADIUS(Sun)', 'MASS(Sun)', 'METALLICITY', 'MET-RATIO', 'SURFACE GRAVITY', 'HB INNER BOUNDARY(au)', 'HB OUTER BOUNDARY(au)', 'SYSTEM DIST.(pc)', 'APPARENT MAG.(v)', 'FUSION ANIM.', 'IMPORTANCE']
  var values = [starName, star_spect, st_teff, st_rad, st_mass, st_met, st_metratio, st_log_gravity, HB_r_i, HB_r_o, sy_dist, sy_vmag,  'Insert anim', 'Very important'];

  // Assign values to each div
  titleDivs.forEach(function(div, index) {
    div.innerHTML = titles[index];
  }); 
  valueDivs.forEach(function(div, index) {
    div.innerHTML = values[index];
  }); 

  //for stop follow object
  stop_follow_btn = document.getElementById('stop-follow')
  stop_follow_btn.addEventListstener('click', function() {
    viz.getViewer().stopFollowingObject()
    viz.getViewer().cameraControls.target.set(0,0,0);
  }); 
}