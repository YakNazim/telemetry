Map {
  background-color: #f6f4f2;
}

#relief {
  raster-opacity: 0.7;
  raster-scaling: bicubic;
}

#shade {
  raster-opacity: 1;
  raster-scaling: bicubic;
  raster-comp-op: color-burn;
}

#contour {
  line-width:0.7;
  line-color:#392b22;
  line-opacity: 0.2;
  line-comp-op: color-burn;
  line-simplify: 0.5;
  line-simplify-algorithm: zhao-saalfeld;
  line-smooth: 0.4;

  [zoom>=10] {
    [ELEV=1200],
    [ELEV=1500],
    [ELEV=1800] {
      line-width: 1.5;
      ::labels {
        text-name: [ELEV];
        text-face-name: "Droid Sans Regular";
        text-placement: line;
        text-spacing: 500;
        text-fill:#392b22;
        text-opacity: 0.6;
        text-halo-fill: #bed993;
        text-halo-radius: 3;
      }
    }
  }

  [zoom>=14] {
    [ELEV=1100],
    [ELEV=1150],
    [ELEV=1200],
    [ELEV=1250],
    [ELEV=1300],
    [ELEV=1350],
    [ELEV=1400],
    [ELEV=1450],
    [ELEV=1500],
    [ELEV=1550],
    [ELEV=1600],
    [ELEV=1650], 
    [ELEV=1700],
    [ELEV=1750],
    [ELEV=1800],
    [ELEV=1850],
    [ELEV=1900],
    [ELEV=1950],
    [ELEV=2000] {
      line-width: 1.5;
      ::labels {
        text-name: [ELEV];
        text-face-name: "Droid Sans Regular";
        text-placement: line;
        text-spacing: 500;
        text-fill:#392b22;
        text-opacity: 0.6;
        text-halo-fill: #bed993;
        text-halo-radius: 3;
      }
    }
  }
  [zoom>=17] {
    line-width: 0.8;
    line-opacity: 0.1;
      ::labels {
        text-name: [ELEV];
        text-face-name: "Droid Sans Regular";
        text-placement: line;
        text-spacing: 500;
        text-fill:#392b22;
        text-opacity: 0.17;
        text-halo-radius: 0;
      }
    }
}

#extra [description='clear'] {
  polygon-fill: #fff;
  polygon-opacity: 0.55;
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
    
    ::labels {
      text-name: [ref];
      text-face-name: "Droid Sans Regular";
      text-placement: line;
      //text-spacing: 1000;
      text-halo-fill: #fe3;
      text-halo-radius: 3;
    }
  }
  
  [highway='track'],
  [highway='service'],
  [highway='residential'],
  [highway='unclassified']{
        line-width: 1.5;
        line-color:#bbb;
    [zoom>=15] {
      ::case {
        line-width: 4;
        line-color:#bbb;
      }
      ::fill {
        line-width: 3;
        line-color:#ddd;
      }
     }
     [zoom>=18] {
      ::case {
        line-width: 9;
        line-color:#bbb;
      }
      ::fill {
        line-width: 8;
        line-color:#ddd;
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
    ::labels {
      text-name: [name];
      text-face-name: "Droid Sans Regular";
      text-placement: line;
      //text-spacing: 1000;
      text-halo-fill: #ccc;
      text-halo-radius: 3;
    }
  }

  [power!='']{
    line-width: 2;
    line-color:#dd26c5;
    line-opacity: 0.4;
    ::labels {
      text-name: [operator];
      text-face-name: "Droid Sans Regular";
      text-placement: line;
      //text-spacing: 1000;
      text-halo-fill: #eee;
      text-halo-radius: 3;
    }
  }
}

#extra {
  [description='road'] {
    line-width: 1.5;
        line-color:#bbb;
    [zoom>=15] {
      ::case {
        line-width: 4;
        line-color:#bbb;
      }
      ::fill {
        line-width: 3;
        line-color:#ddd;
      }
     }
     [zoom>=18] {
      ::case {
        line-width: 9;
        line-color:#bbb;
      }
      ::fill {
        line-width: 8;
        line-color:#ddd;
      }
    }
    [Name='Entrance Road'] {
      ::case {
        line-width: 9;
        line-color:#bdd;
      }
      ::fill {
        line-width: 8;
        line-color:#dff;
      }
    }
  }
  [description='track'] {
    line-width: 3;
    line-color: #ccc;
    line-opacity: 0.4;
  }
  
  [description='trail'] {
    line-width: 2;
    line-color: #ddd;
    line-opacity: 0.4;
  }
  
  [description='ruin'] {
    polygon-fill: #9e713b;
    polygon-opacity: 0.4; 
  }
  
  [description='gate'] {
    marker-fill: #aa6a88;
    marker-line-width: 0;
    marker-type: arrow;
    ::labels {
      text-name: [Name];
      text-face-name: "Droid Sans Regular";
      text-fill: #ccc;
      text-size: 10;
      text-placement: vertex;
    }
  }
}

#extra [description='clear'] {
  [Name='Flight Line'] {
    ::labels {
      text-name: [Name];
      text-face-name: "Droid Sans Regular";
      text-fill: #aa6a88;
      text-size: 13;
      text-placement: interior;
      text-allow-overlap: false;
      }
  }
}
