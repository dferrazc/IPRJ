#include < stdio .h >
#include < math .h >
double Lm [5] = { 0 , 0 , 0 , 0 , 0};
double AB = 0 , BD = 0 , CD = 0 , Lf = 0 , Me = 0 , Ml = 0 , Mc = 0 , D1 = 0 ,D2 = 0 , NAlfa = 0;
double El [5] = { 0 , 0 , 0 , 0 , 0} , Cp [5] = { 0 , 0 , 0 , 0 , 0} , Rxl , Ryl , Rxp, Ryp , Rxt , Ryt ;
double DAlfa = 0;
double We2 = 0 , WAB = 0;
double Alfa = 0 , Beta = 0;

#define mPi acos ( -1)
#define Yel " \ x1B [33 m "
#define Res " \ x1B [0;0 m "
#define Gre " \ x1B [32 m "
#define Red " \ x1b [31;1 m "
#define Ne1 " \ x1b [30;47 m "
#define Ne2 " \ x1b [37 m "
void main ()
{
  printf ( " Digite os valores na " Red " seguinte ordem " Res " AB , BD , CD , Lf , Me, Ml , Mc , D1 , D2 , NAlfa , Lm1 , Lm2 , Lm3 , Lm4 , Lm5 separados por " Red " espa ç o "
Res " e pressione ENTER : \ n " Ne2 ) ;
  scanf ( " % lf % lf % lf % lf % lf % lf % lf % lf % lf % lf % lf % lf % lf % lf % lf ", & AB , & BD , & CD , & Lf , & Me , & Ml , & Mc , & D1 , & D2 , & NAlfa , & Lm [0] , & Lm
[1] , & Lm [2] , & Lm [3] , & Lm [4]) ;
  We2 = ( Me * 9.81) /2;
  Ml = Ml *9.81;
  Mc = Mc *9.81;
  Me = Me *9.81;
  WAB = ( Mc + ( Ml /2) ) /(2* AB ) ;
  DAlfa = ( mPi / D2 - mPi / D1 ) /( NAlfa - 1) ;
  Alfa = mPi / D1 ;
  printf( Yel "\n Alfa " Gre "%f %f %f %f %f \n " Res , Lm [0] , Lm [1] , Lm [2] , Lm [3] , Lm [4]) ;
  for ( int i =0; i < NAlfa ; i ++)
  { 
    for ( int j =0; j <5; j ++)
    {
      Beta = atan (( AB * sin ( Alfa ) + BD ) /( CD - AB * cos ( Alfa ) ) );
      Rxl = ( We2 + (( Lf + Lm [ j ]) * WAB ) ) /( tan ( Alfa ) + tan ( Beta ) );
      Ryl = Rxl * tan ( Beta ) - We2;
      Rxt = 2* Rxl;  
      Ryt = 2* Ryl - ( Mc + Ml );
      Ryp = Ryl + ( Me );
      Rxp = Rxl ;
      El[j] = ((Rxt * sin(Alfa)) + ( Ryt * cos(Alfa)));
      Cp[j] = (Rxp * cos(Beta) + Ryp * sin(Beta));
    }
    printf( " Shear Stress : " Ne2 " %f %f %f %f %f %f " Res " \n", Alfa, El[0], El[1], El[2], El[3], El[4]);
    printf( " Compression:" Ne2 " %f %f %f %f %f %f " Res " \n", Alfa, Cp[0], Cp[1], Cp[2], Cp[3], Cp[4]) ;
    Alfa = Alfa + DAlfa ;
  }
}
