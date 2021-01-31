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
#include "ROOT/TH1D.h"
#include "ROOT/TFile.h"
#include "ROOT/TH2D.h"
#include "ROOT/TH3D.h"
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

void plotRoot(){
 
  gROOT->Reset();
  gROOT->SetStyle("Modern");
  auto style = gROOT->GetStyle("Modern");
  style->SetLineScalePS(1);
  style->cd();
  gROOT->ForceStyle();
  // Draw histos filled by Geant4 simulation 
  //   

  // Open file filled by Geant4 simulation 
 // for(int i = 20;i<=60;i+=10)
//{
  /*char  noa[100];
  char a[100];
  char b[100];
  char c[100];
  char d[100];
  char e[100];
  char g[100];*/
  //sprintf(a,"%d", i);
  //sprintf(b,"%d", i);
  std::vector<std::string> fnames = {"plots/LR-SiPM.svg","plots/LR-SiPM-LOG.svg","plots/Strips.svg","plots/Strips-LOG.svg","plots/PD-Ratio.svg","plots/LeftAndRight.svg","plots/PhotonDeath"};
  std::vector<char*> out;
  for(int i = 0; i<7;i++)
  {
    std::string str = fnames[i];
    char *cstr = new char[str.length() + 1];
    strcpy(cstr, str.c_str());
    out.push_back(cstr);
  }

  //strcat(b,"_B3A.root");
  //TFile f(b);
  TFile f("../build/B3a/B3Atest.root");
  // Create a canvas and divide it into 2x2 pads
  const int nx = 3;
  const int ny = 16;

  std::vector<std::string> nm = {"_Photon-Deposition per gamma-LRDetectors","_Photon-Deposition per gamma-LRDetectors",
  "_Photon-Deposition per gamma-Strips","_Photon-Deposition per gamma-Strips","_Photon-Deposition per gamma-PDRatio","_Photon-Deposition per gamma--Left and Right"};

    std::string cst = "Cross Section (barns-atom-MeV) - ";
    std::string cstT = cst + "Total";
    std::string cstp = cst + "PhotoElectric";
    std::string cstc = cst + "Compton";
    std::string cstr = cst + "Rayleigh";

  std::vector<std::string> n2 = {cstT,cstp,cstc,cstr};
  std::vector<std::string> nmLR = {"_Photon-Deposition per gamma-L","_Photon-Deposition per gamma-R", "Average Photons Detected per interacted gamma for 2D LEFT (n-mm x,y)", "Average Photons Detected per interacted gamma for 2D RIGHT (n-mm x,y)"};
  std::vector<std::string> nmPD = {"Photon Death - Boundary Percent (Internal,Boundary)","Photon Death - Boundary Process List (OpAbs,Transport,Other)","Photon Death 3D (mm x,y,z)"};

  TH1D* hist1;
  TH2D* hist2;
  TH3D* hist3;
  TCanvas* c1;
  //#ifndef CSTS

  for(int iter = 0; iter<6; iter++)
  {  
    if(iter!=5)
    {
      c1 = new TCanvas(out[iter], "Number of Photons in Event (#Events/#Photons)", 0, 0, 3200, 9600);
      c1->Divide(nx,ny);
    }
    else
    {
      c1 = new TCanvas(out[iter], "Number of Photons in Event (#Events/#Photons)", 0, 0, 1600,1600);
      c1->Divide(2,2);      
      auto legend = new TLegend(0.52,0.7,0.9,0.9);
      legend->SetHeader("Legend","C"); // option "C" allows to center the header
      for(int k = 0; k<2; k++)
      { 
        std::string name = nmLR[k];
        char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
        strncpy(cptr, name.c_str(), name.size());
        hist1 = (TH1D*)f.Get(cptr);

        for(int uL = 0; uL<2; uL++)
        { 
          c1->cd(uL+1);
          if(hist1)
          {
            if(uL!=1)
            {
              hist1->SetTitle("L & R");
            }
            else
            {
              gPad->SetLogy(1);
              hist1->SetTitle("L & R LOG");
            }
            if(k==0)
            {
              cout << "BLUE_L"<<endl;
              hist1->SetLineColor(kBlue);
              legend->AddEntry(hist1,"Left Detector","l");
              hist1->Draw("HIST");
            }
            else
            {
              cout << "RED_R"<<endl;
              hist1->SetLineColor(kRed);
              legend->AddEntry(hist1,"Right Detector","l");
              hist1->Draw("SAME HIST");
            }
            c1->Modified();
            c1->Update();
          }
          else
          {
            cout << "ERROR" <<endl;
          }
        }
        for(int uL = 2; uL<4; uL++)
        { 
          c1->cd(uL+1);
          std::string name = nmLR[uL];
          char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
          strncpy(cptr, name.c_str(), name.size());
          hist2 = (TH2D*)f.Get(cptr);
          if(hist2)
          {
            //hist2->SetMarkerSize(2.0);
            hist2->Draw("COLZ TEXT");
            c1->Modified();
            c1->Update();
          }
          else
          {
            cout << "ERROR" <<endl;
          }
        }
        c1->cd(1);
      }
      legend->Draw();
      c1->Print(out[iter]);
      //---6
      iter = 6;
      c1 = new TCanvas(out[iter], "", 0, 0, 1600, 800);
      c1->Divide(3,1);
      for(int i = 0;i<2;i++)
      {
        c1->cd(i+1);
          std::string name = nmPD[i];
          char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
          strncpy(cptr, name.c_str(), name.size());
          hist1 = (TH1D*)f.Get(cptr);
          if(hist1)
          {
            //hist2->SetMarkerSize(2.0);
            hist1->Draw("HIST");
            c1->Modified();
            c1->Update();
          }
          else
          {
            cout << "ERROR" <<endl;
          }
      }
      c1->cd(3);
          std::string name = nmPD[2];
          char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
          strncpy(cptr, name.c_str(), name.size());
          hist3 = (TH3D*)f.Get(cptr);
          if(hist3)
          {
            //hist2->SetMarkerSize(2.0);
            hist3->Draw("");
            c1->Modified();
            c1->Update();
          }
          else
          {
            cout << "ERROR" <<endl;
          }
      c1->Print(out[iter]);
      return;
    }

    if((iter==1)||(iter==3))
    {
      c1->SetName("Number of Photons in Event (#Events/#Photons) (LOG)");
    }

  for(int j = 1; j<=ny; j++)
  {
    for(int i = 1; i<=nx; i++)
    {
      int num = ((j-1)*nx+i);
      c1->cd(num);
      c1->SetMargin(0,0,0,0);

      //char name[100];
      //sprintf(name,"%d", i);
      //sprintf(name,"%d", j);
      //strcat(name,"Photon-Deposition Per gamma (nOfPhotons)");
      //std::cout<<name<<std::endl;

      std::string name = to_string(i)+to_string(ny-j+1)+nm[iter];
      char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
      strncpy(cptr, name.c_str(), name.size());
      if(iter!=4)
      {
        hist1 = (TH1D*)f.Get(cptr);
        if(hist1)
        {
          /*Double_t factor = 1.;
          int ent = hist1->GetEntries();
          if(ent>0)
          {
            hist1->Scale(factor/ent);         
          }*/
          //gPad->SetMargin(0,0,0,0);
          if((iter==1)||(iter==3))
          {
            gPad->SetLogy(1);
            //hist1->GetYaxis()->SetTitle("Gamma Events (LOG)");
          }
          else
          {

            //hist1->GetYaxis()->SetTitle("Gamma Events");
            //hist1->GetYaxis()->SetRangeUser(0,0.2);
          }
          
          //hist1->GetXaxis()->SetTitle("Number of Photons in Event (#)");        
          hist1->Draw("HIST");
          c1->Modified();
          c1->Update();
        }
        else
        {
          std::cout << "ERROR !" <<std::endl;
        }
      }
      else
      {
        hist2 = (TH2D*)f.Get(cptr);
        if(hist2)
        {    
          hist2->Draw("");
          c1->Modified();
          c1->Update();
        }
        else
        {
          std::cout << "ERROR 2D!" <<std::endl;
        }
      }      
    }  
  }
  c1->Print(out[iter]);
  //delete c1;
  }
//#endif
//----------------------------------------
#ifdef CSTS

    c1 = new TCanvas("CrossSection", "", 20, 20, 3200, 6400);
    c1->Divide(2,2);
    //vector<TH1D> hd; 
    int fnum = 0;
    const char *namecs[] = {"NISTT","NISTPh","NISTRay","NISTCpt"};

  for(int j = 0; j<4; j++)
  {
      c1->cd(j+1);
      //hd.push_back(*(new TH1D(namecs[j], namecs[j], n,0.00001,1)));

      std::string name = n2[j];
      char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
      strncpy(cptr, name.c_str(), name.size());

      hist1 = (TH1D*)f.Get(cptr);
      if(hist1)
      {
        gPad->SetLogy(1);
        gPad->SetLogx(1);
        hist1->GetYaxis()->SetTitle("Barns per atom (LOG)");
        hist1->GetXaxis()->SetTitle("MeV (LOG)");        
        hist1->GetYaxis()->SetRangeUser(0.01,100000000);
        hist1->GetXaxis()->SetRangeUser(0.00001,1);
        hist1->Draw("HIST");
        c1->Modified();
        c1->Update();
      }
      else
      {
        cout << "ERROR !" <<endl;
      }
      /*  if(j==0)
      {
        Double_t x[4000] = {};
        Double_t y[4000] = {};
        int n = 25;//1001
        TH1D* hd = new TH1D("NISTT","NISTTID", n ,0.00001,1);
        //ifstream myfile("lambdas5.txt", ios_base::app);
        //ifstream myfile("barns20.txt", ios_base::app);
        ifstream myfile("PVT_FULL.txt", ios_base::app);
        string line;
        double gperatom = 1.023*pow(10,3)/(6.022*19);
        char delm = ' ';
        for (Int_t i=0;i<n;i++) {
          getline (myfile,line);
			    vector<string> val = split(line,delm);
			    double en = double(stod(val[0]));
			    //double att_CS = 1/double(stod(val[1])); //photo
          double att_CS = double(stod(val[7])); //nist (total = 7, photo = 1, rayleigh = 2, compt = 3)
			    x[i] = en;y[i] = att_CS*gperatom;
          //x[i] = en;y[i] = double(stod(val[1]));
          hd->Fill(x[i],y[i]);
        }
        myfile.close();
        //TGraph* gr = new TGraph(n,x,y);
        //gr->Draw("AC*");
        //gPad->SetLogy(1);
        //gPad->SetLogx(1);
        //hd->GetYaxis().SetTitle("Barns per atom (LOG)");
        //hd->GetXaxis().SetTitle("MeV (LOG)");        
        //hd->GetYaxis().SetRangeUser(0.01,100000000);
        //hd->GetXaxis().SetRangeUser(0.00001,1);
        hd->SetMarkerStyle(kFullCircle);
        hd->Draw("SAME P");
        cout<<"drawn"<<endl;
        c1->Modified();
        c1->Update();
      }*/
  
  }
  c1->Print("CrossSection.pdf");
  #endif
}

  /*
  c1->Divide(2,3);

  // Draw Eabs histogram in the pad 1

  c1->cd(1);
  TH1D* hist1 = (TH1D*)f.Get("EDep");
  hist1->Draw("HIST");
  
  // Draw Labs histogram in the pad 2
  c1->cd(2);
  gPad->SetLogy(1);
  //TH1D* hist2 = (TH1D*)f.Get("Labs");
  hist1->Draw("HIST");
  

  c1->cd(3);
  TH1D* hist4 = (TH1D*)f.Get("EDep2D");
  hist4->Draw("COLZ");
  // Draw Egap histogram in the pad 3
  // with logaritmic scale for y
  TH1D* hist3 = (TH1D*)f.Get("Energy-netfraction");
  c1->cd(4);
  gStyle->SetEndErrorSize(0.001);
  hist3->SetMarkerStyle(20);
  hist3->SetMarkerColor(kRed);
  hist3->Draw("E1");
  

  c1->cd(5);
  TH1D* hist5= (TH1D*)f.Get("Dose");
  hist5->Draw("HIST");

  c1->cd(6);
  TH1D* hist6 = (TH1D*)f.Get("E-Deposition Total");
  hist6->Draw("HIST");
  // Draw Lgap histogram in the pad 4
  // with logaritmic scale for y
*/
 
//} 
/*int main(){
    plotCD();
    return 0;
}*/