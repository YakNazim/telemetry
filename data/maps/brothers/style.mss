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
  line-comp-op: color-burn;
  [CONTOURELE=4200],
  [CONTOURELE=4300],
  [CONTOURELE=4400],
  [CONTOURELE=4500],
  [CONTOURELE=4600], 
  [CONTOURELE=4700], 
  [CONTOURELE=4800], 
  [CONTOURELE=4900], 
  [CONTOURELE=5000], 
  [CONTOURELE=5100], 
  [CONTOURELE=5200],
  [CONTOURELE=5300], 
  [CONTOURELE=5400] {
  line-width: 1.5;
    ::labels {
      text-name: [CONTOURELE];
      text-face-name: "Droid Sans Regular";
      text-placement: line;
      text-ratio: 3;
      text-fill:#392b22;
      text-opacity: 0.6;
      text-halo-fill: #bed993;
      text-halo-radius: 3;
      text-max-char-angle-delta: 40;
    }
  }
}

#roads {
  line-width:0;

  [name='Central Oregon Highway'] {
    ::case {
      line-width: 4;
      line-color:#d83;
    }
    ::fill {
      line-width: 3;
      line-color:#fe3;
    }
    [zoom>=15] {
      ::case {
        line-width: 8;
        line-color:#d83;
      }
      ::fill {
        line-width: 6;
        line-color:#fe3;
      }
    }
    [zoom>=19] {
      ::case {
        line-width: 11;
        line-color:#d83;
      }
      ::fill {
        line-width: 9.5;
        line-color:#fe3;
      }
    }
  }
  
  [highway='track'],
  [highway='service'],
  [highway='residential'],
  [highway='unclassified']{
        line-width: 1;
        line-color:#ddd;
    [zoom>=15] {
      ::case {
        line-width: 4;
        line-color:#ccc;
      }
      ::fill {
        line-width: 3;
        line-color:#eee;
      }
     }
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
    line-width: 2;
    line-color: #666;
  }

  [power!='']{
    line-width: 2;
    line-color:#dd26c5;
    line-opacity: 0.4;
  }
}