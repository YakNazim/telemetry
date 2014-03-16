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
