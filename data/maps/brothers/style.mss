Map {
  background-color: #f6f4f2;
}

#elevation {
  raster-opacity: 0.7;
  raster-scaling: bicubic;
}

#slope {
  raster-opacity:1;
  raster-scaling: bicubic;
  raster-comp-op: multiply;
}

#contour {
  line-width:0.7;
  line-color:#392b22;
  line-opacity: 0.2;
  line-smooth: 1;
  line-comp-op: color-burn;
}


#roads {
  line-width:0;

  [highway='track'],
  [highway='service'],
  [highway='residential'],
  [highway='unclassified']{
    line-width: 1;
    line-color:#ccc;
  }
  
  [name='Central Oregon Highway'] {
    line-width: 5;
    line-color: #f00;
  }
  
  [name='Moffitt Road'],
  [name='Fox Butte Road'],
  [name='Montgomery Road'],
  [name='Coffey Road'],
  [name='Crooked River Highway'],
  [name='Fox Tail Butte Road'],
  [name='Newt Morris Road'],
  [name='Camp Creek Road'],
  [name='Frederick Butte Road'] {
    line-width: 3;
    line-color: #666;
  }

  [power!='']{
    line-width: 2;
    line-color:#dd26c5;
    line-opacity: 0.5
  }
}