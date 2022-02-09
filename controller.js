var stage = 0;

function keyPress(e){
	pressed = false;
    if (e.key === "n"){
		stage++;
		pressed = true;
	}
	if (e.key === "p"){
		stage--;
		pressed = true;
	}
	if (stage<0){
		stage = 0;
	}
	if (stage>maxStage){
		stage = maxStage;
	}
	if (pressed===true){
		document.getElementById(`scroll${stage}`).scrollIntoView({behavior: "smooth"});
	}
}
document.addEventListener('keydown', keyPress);