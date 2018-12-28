rocket rocket = new rocket();
int angle = 0;
float scalefactor = 0.7;
//float x = 0;
//float y = 0;
//float z = 1800;
float a = 0;
float b = 0;
float c = 0;
float[] subjectp = new float[3];
float[] subjecto = new float[3];
PVector[] datap = new PVector[100000000];
PVector[] datao = new PVector[100000000];
//x,y,z,a,b,c = scalefactor;


void setup () {
  size(600, 600, P3D);
  background(150, 150, 255);
  translate(width/2, height/2, 0); 

  String[] positions = loadStrings("positions.txt");
  String[] orientations = loadStrings("orientations.txt");


  for (int i = 0; i < positions.length-1; i++) {
    String[] datapointp = split(positions[i], ',');
    String[] datapointo = split(orientations[i], ',');

    for (int j = 0; j < datapointp.length; j++) {
      subjectp[j] = round(float(datapointp[j])/scalefactor);
      subjecto[j] = float(datapointo[j]);
    }
    datap[i] = new PVector(subjectp[0], subjectp[1], subjectp[2]);
    datao[i] = new PVector(subjecto[0], subjecto[1], subjecto[2]);
  }
  frameRate(10);
}

void draw () {
  //datap[frameCount] = new PVector(datap[0].x, datap[0].y, datap[0].z);
  //datao[frameCount] = new PVector(datao[0].x, datao[0].y, datao[0].z);
  rocket.makedroneship();

  if (-(datap[frameCount+1].z - datap[frameCount].z) > -(datap[frameCount].z - datap[frameCount-1].z)) {
    rocket.make(datap[frameCount].x, datap[frameCount].y, datap[frameCount].z, datao[frameCount].x, datao[frameCount].y, datao[frameCount].z,true);
  } else {
    rocket.make(datap[frameCount].x, datap[frameCount].y, datap[frameCount].z, datao[frameCount].x, datao[frameCount].y, datao[frameCount].z,false);
  }


  //rocket.make(0, 0, frameCount*2, 0, 0, 0,true);
  perspective(PI/3, float(width)/float(height), (height/2.0) / tan(PI/6.0)/10.0, 100000);
  if (mousePressed) {
    camera(3*width*cos(map(mouseX, 0, width, 0, 2*PI)), 3*width*sin(map(mouseX, 0, width, 0, 2*PI)), -height, 0, 0, map(mouseY, 0, height, -10000, 0), 0, 0, 1);
  } else {
    camera(datap[frameCount].x+width*cos(map(mouseX, 0, width, 0, PI)), datap[frameCount].y+ width*sin(map(mouseX, 0, width, 0, PI))*sin(map(mouseY, 0, height, -PI/2, PI/2)), -(height)*cos(map(mouseY, 0, height, 0, PI))-datap[frameCount].z, datap[frameCount].x, datap[frameCount].y, -datap[frameCount].z -100, 0, 0, 1);
  }
}
