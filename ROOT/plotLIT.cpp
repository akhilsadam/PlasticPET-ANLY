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

void plotLIT(){
 
  gROOT->Reset();
  gROOT->SetStyle("Modern");
  
  // Draw histos filled by Geant4 simulation 
  //   

  // Open file filled by Geant4 simulation 
 // for(int i = 20;i<=60;i+=10)
//{

  char a[100];
  char b[100];
  char c[100];
  char d[100];
  //sprintf(a,"%d", i);
  //sprintf(b,"%d", i);
  strcat(a,"LitPlots.pdf");
  strcat(b,"individualLRD-LOG.pdf");
  strcat(c,"individualStrips.pdf");
  strcat(d,"individualStrips-LOG.pdf");
  //strcat(b,"_B3A.root");
  //TFile f(b);
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
  // Create a canvas and divide it into 2x2 pads
  const int nx = 2;
  const int ny = 2;

  std::vector<std::string> nm = {R"(Average Photons Detected per interacted gamma for 2D LEFT (n/mm x,y))",R"(Average Photons Detected per interacted gamma for 2D RIGHT (n/mm x,y))",R"(LIT Probability 2D (n/mm x,y))", R"(# of photons at Left vs Right dets. for LIT strips (n/mm x,y))"};

  std::vector<char*> out = {a,b,c,d};

  TH2D* hist1;
  TCanvas* c1;

 //#ifndef CSTS


  for(int iter = 0; iter<1; iter++)
  {  
    c1 = new TCanvas(out[iter], "", 20, 20, 1600, 1600);
    c1->Divide(nx,ny);
    for(int i = 0; i<(nx*ny); i++)
    {
      c1->cd(i);

      std::string name = nm[i];
      cout << name << endl;
      char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
      strncpy(cptr, name.c_str(), name.size());
      hist1 = (TH2D*)f.Get(cptr);
      if(hist1)
      {
        /*Double_t factor = 1.;
        int ent = hist1->GetEntries();
        if(ent>0)
        {
          hist1->Scale(factor/ent);         
        }*/

        /*if((iter==1)||(iter==3))
        {
          //gPad->SetLogy(1);
          //hist1->GetYaxis()->SetTitle("Gamma Events (LOG)");
        }
        else
        {
          //hist1->GetYaxis()->SetTitle("Gamma Events");
          //hist1->GetYaxis()->SetRangeUser(0,0.2);
        }*/
        
        //hist1->GetXaxis()->SetTitle("Number of Photons in Event (#)");        
        hist1->Draw("COLZ");
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

int main(){
    plotLIT();
    return 0;
}