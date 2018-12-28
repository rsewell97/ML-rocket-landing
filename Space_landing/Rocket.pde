
public class rocket {
  int h = 200;
  int r = 5;
  int sides = 10;

  void make(float x, float y, float z, float a, float b, float c, boolean flame) {
    {
      strokeWeight(0.3);
      fill(240, 240, 240);
      float angle = 0;
      float angleIncrement = TWO_PI / sides;
      translate(x, y, -z);
      rotateX(a*PI/2);
      rotateY(b*PI/2);
      rotateZ(c*PI/2);
      beginShape(QUAD_STRIP);
      for (int i = 0; i < sides + 1; ++i) {
        vertex(r*cos(angle), r*sin(angle), -h);
        vertex(r*cos(angle), r*sin(angle), 0);
        angle += angleIncrement;
      }
      endShape();
      fill(0);
      ellipse(0, 0, 2*r, 2*r);  //engine
      if (flame == true) {
        fill(232, 71, 2);
        beginShape(TRIANGLE_FAN);
        vertex(0, 0, 50);
        vertex(3, 0, 0);
        vertex(0, 3, 0);
        vertex(-3, 0, 0);
        vertex(0, -3, 0);
        vertex(3, 0, 0);
        endShape();
        fill(247, 136, 9,100);
        beginShape(TRIANGLE_FAN);
        vertex(0, 0, 100);
        vertex(7, 0, 0);
        vertex(0, 7, 0);
        vertex(-7, 0, 0);
        vertex(0, -7, 0);
        vertex(7, 0, 0);
        endShape();
      }
      fill(0);
      translate(0, 0, -15);    //landing legs
      box(2, 14, 30);
      box(14, 2, 30);
      translate(0, 0, -h+20);
      fill(60, 100);          //gridfins
      box(25, 4, 2);
      box(4, 25, 2);
      translate(0, 0, -5);
      fill(200);
      ellipse(0, 0, 2*r, 2*r);
      translate(1, r, h-10);      
      rotateX(-a*PI/2);
      rotateY(-b*PI/2);
      rotateZ(-c*PI/2);
      translate(-x, -y, z);
      directionalLight(220, 200, 200, -1, 0, 0);
    }
  }
  void makedroneship() {
    noStroke();
    rectMode(CENTER);
    background(150, 150, 255);
    fill(80, 80, 255);
    translate(0, 0, 1);
    rect(0, 0, 2000*width, 2000*height);

    translate(0, 0, -1);    
    fill(20, 20, 20);
    rect(0, 0, 100, 100);
  }
  void update(float x, float y, float z, float vx, float vy, float vz) {
    x += vx;
    y += vy;
    z += vz;
    //this.rocket(translate(vx,vy,vz));
  }
}
