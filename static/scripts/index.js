function build_table(){
    let table = document.getElementById('squares')
    let htmlnew = ''
    for(let tr=0; tr<30; tr++){
        htmlnew += `<tr class="row" id="row_${tr}">`
        for(let td=0; td<40; td++){
            htmlnew += `<td class="col" id="${tr}-${td}"></td>`
        }
        htmlnew += `</tr>`
    }
    table.innerHTML += htmlnew;
    let tableParent = document.getElementById('table')
    tableParent.style.height = `${document.getElementById('image').offsetHeight}px`;
}

function update_path(){
    let Ax = document.getElementById('input_Ax').value 
    let Ay = document.getElementById('input_Ay').value 
    let Bx = document.getElementById('input_Bx').value 
    let By = document.getElementById('input_By').value 
    if (!(Ax && Ay && Bx && By)){
        return;
    }
    let A = document.getElementById(`${Ay}-${Ax}`)
    let B = document.getElementById(`${By}-${Bx}`)

    A.style.backgroundImage = `url("/static/images/aPoint.png")`
    B.style.backgroundImage = `url("/static/images/bPoint.png")`

    window.location.href = `/${Ax}-${Ay}-${Bx}-${By}`
}   

function color_by_n(n){
    return colors[n]
}

function render_anomalies(map){
    for(let x=0; x<30; x++){
        for(let y=0; y<40; y++){
            let cell = document.getElementById(`${x}-${y}`)
            
            cell.style.backgroundColor = `${color_by_n(map[x][y])}`;
            cell.style.opacity = '0.2'
            
        }
    }
}

function build_path(path){
    if (path.length == 0){
        return
    }
    for(let point of path){
        let cell = document.getElementById(`${point[0]}-${point[1]}`)
        cell.style.backgroundColor = 'white'
        cell.style.opacity = '1'
    }
    
}


function newan(){
    let x = document.getElementById('input_Ix').value;
    let y = document.getElementById('input_Iy').value;
    let int0 = document.getElementById('input_Int').value;
    window.location.href = `/r-${x}-${y}-${int0}`

}

let colors = [
    "#000000",
    "#ff1100",
    "#ff2600",
    "#ff3700",
    "#ff4800",
    "#ff5900",
    "#ff6f00",
    "#ff8000",
    "#ff9100",
    "#ffa600",
    "#ffb700",
    "#ffc800",
    "#ffd900",
    "#ffee00",
    "#ffff00",
    "#eeff00",
    "#d9ff00",
    "#c8ff00",
    "#b7ff00",
    "#a6ff00",
    "#91ff00",
    "#80ff00",
    "#6fff00",
    "#59ff00",
    "#48ff00",
    "#37ff00",
    "#26ff00",
    "#11ff00",
    "#00ff00",
    "#00ff11",
    "#00ff26",
    "#00ff37",
    "#00ff48",
    "#00ff59",
    "#00ff6f",
    "#00ff80",
    "#00ff91",
    "#00ffa6",
    "#00ffb7",
    "#00ffc8",
    "#00ffd9",
    "#00ffee",
    "#00ffff",
    "#00eeff",
    "#00d9ff",
    "#00c8ff",
    "#00b7ff",
    "#00a6ff",
    "#0091ff",
    "#0080ff",
    "#006fff",
    "#0059ff",
    "#0048ff",
    "#0037ff",
    "#0026ff",
    "#0011ff",
    "#0000ff",
    "#1100ff",
    "#2600ff",
    "#3700ff",
    "#4800ff",
    "#5900ff",
    "#6f00ff",
    "#8000ff",
    "#9100ff",
    "#a600ff",
    "#b700ff",
    "#c800ff",
    "#d900ff",
    "#ee00ff",
    "#ff00ff",
]
