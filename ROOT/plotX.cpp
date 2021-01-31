// ROOT macro file for plotting example B4 histograms 
// 
// Can be run from ROOT session:
// root[0] .x plotHisto.C
using namespace std;
#include <vector>
#include <iostream>
#include <fstream>
#include <iomanip>
#include "ROOT/RConfigure.h"
#include "ROOT/ROOT/RConfig.hxx"
#include "ROOT/RConfig.h"
#include "ROOT/TObject.h"
#include "ROOT/TROOT.h"
#include "ROOT/TTree.h"
#include "ROOT/TKey.h"
#include "ROOT/TH1D.h"
#include "ROOT/TFile.h"
#include "ROOT/TH2D.h"
#include "ROOT/TF1.h"
#include "ROOT/TGraph.h"
#include "ROOT/TCanvas.h"
//g++ plotRoot.cpp -o plotRoot -I /home/mitt-unix/../../usr/include/ROOT/ -std=c++17

#define CSTS

vector<string> split (const string &s, char delim) 
{
    vector<string> result;
    stringstream ss (s);
    string item;

    while (getline (ss, item, delim)) {
        result.push_back (item);
    }

    return result;
}

void plotX(){
 
  gROOT->Reset();
  gROOT->SetStyle("Modern");
  
  // Draw histos filled by Geant4 simulation 
  //   

  // Open file filled by Geant4 simulation 
 // for(int i = 20;i<=60;i+=10)
//{
  char NA[100];
  char a[100];
  char b[100];

  strcat(a,"XPredictor.pdf");
  strcat(b,"XPredictorNormal.pdf");
  
  TFile f("../build/B3a/B3Atest.root");
  /*TList L = f.GetSeekParent
  L.Print();
  int nhist=0;
  for(TObject* key0 : L) {
    nhist++;
    cout << "Key " << nhist << endl;
    cout << " Classname " <<key0->GetTitle() << endl;
    cout << " Title " << endl;
  }*/
 
  std::vector<std::string> nm = {R"((L-R) Photon Ratio as X-Predictor (ln(LR Ratio) by m))","(L-R) Photon Ratio as X-Predictor"};

  std::vector<char*> out = {a,b};

  TH1D* hist1;
  TH2D* hist2;
  TCanvas* c1;

 //#ifndef CSTS


  for(int iter = 0; iter<2; iter++)
  {  
    c1 = new TCanvas(out[iter], "", 20, 20, 1600, 1600);
    std::string name = nm[iter];
    cout << name << endl;
    char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
    cptr[name.size()] = '\0';
    strncpy(cptr, name.c_str(), name.size());
    cout << cptr << endl;
    if(iter==0)
    {
      hist2 = (TH2D*)f.Get(cptr);
      if(hist2)
      {
        TF1 *f1 = new TF1("f1","[0]+[1]*x",0,1);
        f1->SetParameters(0.,1.);
        f1->SetLineColor(kRed);
        hist2->Fit(f1);
        hist2->Draw("COLZ");
        f1->Draw("same");
        c1->Modified();
        c1->Update();
      }
      else
      {
        std::cout << "ERROR !" <<std::endl;
      }
    }
    if(iter!=0)
    {
      hist1 = (TH1D*)f.Get(cptr);
      if(hist1)
      {
        TF1 *f1 = new TF1("f1","gausn(0)",0,1);
        f1->SetParameters(1.,0.,1.);
        f1->SetLineColor(kRed);
        hist1->Fit(f1);
        hist1->Draw("");
        f1->Draw("same");
        c1->Modified();
        c1->Update();
      }
      else
      {
        std::cout << "ERROR !" <<std::endl;
      }
    }
    
    c1->Print(out[iter]);
  }
}
