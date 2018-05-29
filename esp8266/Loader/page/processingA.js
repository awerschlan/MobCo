var srcBox,srcImg,dstImg;
var epdArr,epdInd,palArr;
var curPal;
function getElm(n){return document.getElementById(n);}
function setInn(n,i){ document.getElementById(n).innerHTML=i;}

function processFiles(files){
    var file=files[0];
    var reader=new FileReader();
    srcImg=new Image();
    reader.onload=function(e){
        setInn('srcBox','<img id=\"imgView\" class=\"sourceImage\">');
        var img=getElm('imgView');
        img.src=e.target.result;
        srcImg.src=e.target.result;
    };
    
    reader.readAsDataURL(file);
}
//-------------------------------------------
function drop(e){
    e.stopPropagation();
    e.preventDefault();
    var files=e.dataTransfer.files;
    processFiles(files);
}
//-------------------------------------------
function ignoreDrag(e){
    e.stopPropagation();
    e.preventDefault();
}
//-------------------------------------------
function getNud(nm,vl){
    return '<td class=\"comment\">'+nm+':</td>'+
    '<td><input id=\"nud_'+nm+'\" class=\"nud\"type=\"number\" value=\"'+vl+'\"/></td>';
}
//-------------------------------------------
function Btn(nm,tx,fn){
    return '<div><label class=\"menu_button\" for=\"_'+nm+'\">'+tx+'</label>'+
    '<input class=\"hidden_input\" id=\"_'+nm+'\" type=\"'+
    (nm==0?'file\" onchange=\"':'button\" onclick=\"')+fn+'\"/></div>';
}
//-------------------------------------------
function RB(vl,tx){
    return ((vl%3)>0?' ':'<br>') + '<input type=\"radio\" name=\"kind\" value=\"m'+vl+
	'\" onclick=\"rbClick('+vl+');\"'+(vl==0?'checked=\"true\"':'')+'/>'+tx;
}
//-------------------------------------------
window.onload = function(){
    srcBox = getElm('srcBox');
    srcBox.ondragenter=ignoreDrag;
    srcBox.ondragover=ignoreDrag;
    srcBox.ondrop=drop;
    srcImg=0;
    epdInd=0;
  
palArr=[[[0,0,0],[255,255,255]],
[[0,0,0],[255,255,255],[255,0,0]],
[[0,0,0],[255,255,255],[127,127,127]],
[[0,0,0],[255,255,255],[127,127,127],[255,0,0]],
[[0,0,0],[255,255,255]],
[[0,0,0],[255,255,255],[220,180,0]]];
  
epdArr=[[200,200,0],[200,200,3],[152,152,5],
[122,250,0],[104,212,1],[104,212,5],
[176,264,0],[176,264,1],[176,264,5],
[128,296,0],[128,296,1],[128,296,5],
[400,300,0],[400,300,1],[400,300,5],
[640,384,0],[640,384,1],[640,384,5]];
  
setInn('BT',
Btn(0,'Select image file','processFiles(this.files);')+
Btn(1,'Level: mono','procImg(true,false);')+
Btn(2,'Level: color','procImg(true,true);')+
Btn(3,'Dithering: mono','procImg(false,false);')+
Btn(4,'Dithering: color','procImg(false,true);')+
Btn(5,'Upload image','uploadImage();'));

setInn('XY',getNud('x','0')+getNud('y','0'));
setInn('WH',getNud('w','200')+getNud('h','200'));
  
setInn('RB',RB(0,'1.54')+RB(1,'1.54b')+RB(2,'1.54c')+
RB(3,'2.13')+RB(4,'2.13b')+RB(5,'2.13c')+
RB(6,'2.7&ensp;')+RB(7,'2.7b&ensp;')+
RB(9,'2.9&ensp;')+RB(10,'2.9b&ensp;')+RB(11,'2.9c&ensp;')+
RB(12,'4.2&ensp;')+RB(13,'4.2b&ensp;')+RB(14,'4.2c&ensp;')+
RB(15,'7.5&ensp;')+RB(16,'7.5b&ensp;')+RB(17,'7.5c&ensp;')); 
}
//-------------------------------------------
function rbClick(index){
    getElm('nud_w').value=""+epdArr[index][0];
    getElm('nud_h').value=""+epdArr[index][1];
    epdInd=index;
}