// ROOT macro file for plotting example B4 histograms 
// 
// Can be run from ROOT session:
// root[0] .x plotHisto.C
#include <vector>
using namespace std;
#define CSTS
{
 
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
  strcat(a,"individualLRD.pdf");
  strcat(b,"individualLRD-LOG.pdf");
  strcat(c,"individualStrips.pdf");
  strcat(d,"individualStrips-LOG.pdf");
  //strcat(b,"_B3A.root");
  //TFile f(b);
  TFile f("B3Atest.root");
  // Create a canvas and divide it into 2x2 pads
  const int nx = 3;
  const int ny = 4;

  std::vector<std::string> n = {"_Photon-Deposition per gamma-LRDetectors","_Photon-Deposition per gamma-LRDetectors",
  "_Photon-Deposition per gamma-Strips","_Photon-Deposition per gamma-Strips"};

    std::string cst = "Cross Section (barns-atom-MeV) - ";
    std::string cstT = cst + "Total";
    std::string cstp = cst + "PhotoElectric";
    std::string cstc = cst + "Compton";
    std::string cstr = cst + "Rayleigh";

  std::vector<std::string> n2 = {cstT,cstp,cstc,cstr};

  std::vector<char*> out = {a,b,c,d};

  TH1D* hist1;
  TCanvas* c1;



  for(int iter = 0; iter<4; iter++)
  {  
    c1 = new TCanvas(out[iter], "", 20, 20, 1600, 1600);
    c1->Divide(nx,ny);
  for(int j = 1; j<=ny; j++)
  {
    for(int i = 1; i<=nx; i++)
    {
      int num = ((j-1)*nx+i);
      c1->cd(num);
      

      //char name[100];
      //sprintf(name,"%d", i);
      //sprintf(name,"%d", j);
      //strcat(name,"Photon-Deposition Per gamma (nOfPhotons)");
      //std::cout<<name<<std::endl;

      std::string name = to_string(i)+to_string(ny-j+1)+n[iter];
      char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
      std::strncpy(cptr, name.c_str(), name.size());

      hist1 = (TH1D*)f.Get(cptr);
      if(hist1)
      {
        /*Double_t factor = 1.;
        int ent = hist1->GetEntries();
        if(ent>0)
        {
          hist1->Scale(factor/ent);         
        }*/

        if((iter==1)||(iter==3))
        {
          gPad->SetLogy(1);
          hist1->GetYaxis()->SetTitle("Gamma Events (LOG)");
        }
        else
        {
          hist1->GetYaxis()->SetTitle("Gamma Events");
          //hist1->GetYaxis()->SetRangeUser(0,0.2);
        }
        
        hist1->GetXaxis()->SetTitle("Number of Photons Event Density (#phot/interacted)");        
        hist1->Draw("HIST");
        c1->Modified();
        c1->Update();
      }
      else
      {
        std::cout << "ERROR !" <<std::endl;
      }
  
      
    }  
  }
  c1->Print(out[iter]);
  }

//----------------------------------------
#ifdef CSTS

    c1 = new TCanvas("CrossSection", "", 20, 20, 1600, 1600);
    c1->Divide(2,2);


  for(int j = 0; j<4; j++)
  {
      c1->cd(j+1);
      

      std::string name = n2[j];
      char *cptr = new char[name.size()+1]; // +1 to account for \0 byte
      std::strncpy(cptr, name.c_str(), name.size());

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
        Double_t x[4000], y[4000];
        Int_t n = 2002;
        std::ifstream myfile("lambdas5.txt", std::ios_base::app);
        string line;
        char delm = ' ';
        for (Int_t i=0;i<n;i++) {
          getline (myfile,line)
			    vector<string> val = split(line,delm);
			    double en = double(stod(val[0]));
			    double att_CS = double(stod(val[4]));
			    double att_l = 1/(1.023*att_CS);
			    x[i] = en;y[i] = att_l
        }
        myfile.close();
        TGraph* gr = new TGraph(n,x,y);
        gr->Draw("AC*");
        std::cout << "ERROR !" <<std::endl;
      }
  
  }
  c1->Print("CrossSection.pdf");
#endif
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
}  
