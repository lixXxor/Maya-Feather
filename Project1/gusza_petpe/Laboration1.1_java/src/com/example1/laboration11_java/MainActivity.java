package com.example1.laboration11_java;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.os.Bundle;
import android.support.v4.view.GravityCompat;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.os.Build;
import android.widget.*;
import android.widget.RelativeLayout.LayoutParams;
import android.graphics.Color;
import android.graphics.Path.FillType;
import android.widget.EditText;
import java.lang.Object;


public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
	  super.onCreate(savedInstanceState);
	  Button myButton = new Button(this);
	  myButton.setText("KNAPP");
//	  myButton.setWidth(600);
	  //myButton.setWidth(RelativeLayout.LayoutParams.WRAP_CONTENT);

	  
	  EditText edtField = new EditText(this);
	  edtField.setHint("Text Fält");
	  

	  RatingBar ratingStar = new RatingBar(this);
	  ratingStar.setNumStars(5);
	  
	  
	  EditText editText = new EditText(this);
	  editText.setText("ett text fält som\nklarar\nav\nflera rader\noch använder det utrymme som\n\nfinns");
	  
	  
//        RelativeLayout myLayout = new RelativeLayout(this);
      	LinearLayout mLayout = new LinearLayout(this);
      	mLayout.setOrientation(LinearLayout.VERTICAL);
      	mLayout.setGravity(Gravity.CENTER_HORIZONTAL);
//    	layoutRight.setWeightSum(0.75f);
//      mLayout.setLayoutParams(new LayoutParams(LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT));

        myButton.setId(1);
        edtField.setId(2);
        editText.setId(3);
        
     
	        
//        LinearLayout lStar = new LinearLayout(this);
//        	lStar.setOrientation(LinearLayout.HORIZONTAL);
//        	lStar.setGravity(Gravity.CENTER);
//		  	lStar.setLayoutParams(new LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT));
//		  	lStar.addView(ratingStar);
		  	  	

//        RelativeLayout.LayoutParams buttonParams = 
//                new RelativeLayout.LayoutParams(
//                    RelativeLayout.LayoutParams.MATCH_PARENT, 
//                    RelativeLayout.LayoutParams.WRAP_CONTENT);
//        
////        buttonParams.addRule(RelativeLayout.CENTER_HORIZONTAL);
//
//        RelativeLayout.LayoutParams textParams = 
//                new RelativeLayout.LayoutParams(
//                    RelativeLayout.LayoutParams.MATCH_PARENT,   
//                    RelativeLayout.LayoutParams.WRAP_CONTENT);
        
//        textParams.setMargins(0, 80, 0, 0);

        LinearLayout.LayoutParams starParams = 
                new LinearLayout.LayoutParams(
                		LinearLayout.LayoutParams.WRAP_CONTENT,   
                		LinearLayout.LayoutParams.WRAP_CONTENT);

//        starParams.setMargins(0, 120, 0, 0);
//        starParams.addRule(RelativeLayout.CENTER_IN_PARENT, -1);
        
//        LinearLayout.LayoutParams starParam = 
//                new LinearLayout.LayoutParams(
//                		LinearLayout.LayoutParams.WRAP_CONTENT,   
//                		LinearLayout.LayoutParams.WRAP_CONTENT,
//                		LinearLayou);
//  
        
        RelativeLayout.LayoutParams editTextParams = 
                new RelativeLayout.LayoutParams(
                    RelativeLayout.LayoutParams.MATCH_PARENT,   
                    RelativeLayout.LayoutParams.MATCH_PARENT);
        
//        editTextParams.setMargins(0, 200, 0, 0);
        
        mLayout.addView(myButton);
        mLayout.addView(edtField);
        mLayout.addView(ratingStar, starParams);
        mLayout.addView(editText, editTextParams);
  
        setContentView(mLayout);
	}

}