clear all;
clc all;

#- Constante
Pi    =    acos(-1);

#- Dados de Entrada

Desf  = input("Diâmetro da Esfera: ");  #- Diâmetro da Esfera   (m)
Rho   = input("Densidade da Esfera: "); #- Densidade da Esfera  (kg/m³)
H     = input("Altura do Avião: ");     #- Altura do Avião      (m)
Alpha = input("Inclinação do Avião: "); #- Inclinação do Avião  (Graus)
v0    = input("Velocidade do Avião: "); #- Velocidade do Avião  (km/h)
Theta = input("Angulo das correntes de ar: ");      #- Inclinação do Vento
U0    = input("Velocidade das correntes de ar: ");  #- Velocidade na altura de referência do Vento (m/s)

#--------------------------------------------------------------------------

R     =        287.058; #- Constante para cálculos da densidade do ar
A     = Pi*(Desf**2)/4; #- m²
g     =           9.81; #- Aceleração da gravidade

u     =                                1.68E-5;   #- Viscosidade do Ar
Mesf  =              (Rho*(4/3)*Pi*(Desf/2)^3);   #- Massa da Esfera
V0    =  [0 v0*cosd(Alpha) v0*sind(Alpha)]/3.6;   #- Velocidade do Avião
Fp    =                          [0 0 -Mesf*g];   #- Força Peso

#- Cálculo do número de Reynolds

function CD = gCD(ReD)
    CD   =  zeros(1,columns(ReD));
    CD  += (ReD <= 0.01) .* (4.5+24.*(ReD.^(-1)));
    CD  += (ReD<=20 & ReD > 0.01).*((24.*(ReD.^(-1)).*(1+0.1315.*(ReD.^(0.82-0.05.*log10(ReD))))));
    CD  += (ReD<=260 & ReD > 20).*((24.*(ReD.^(-1))).*(1+0.19355.*(ReD.^0.6305)));
    CD  += (ReD<=1.5E3 & ReD > 260).*(10 .^(1.6435-1.1242 .*log10(ReD)+0.1558.*(log10(ReD).^2)));
    CD  += (ReD<=1.2E4 & ReD > 1.5E3).*((10).^(-2.4571+2.5558.*log10(ReD)-0.9295.*(log10(ReD).^2)+0.1049.*(log10(ReD).^3)));
    CD  += (ReD<=4.4E4 & ReD > 1.2E4).*((10).^(-1.9181+0.6370.*log10(ReD)-0.0636.*(log10(ReD).^2)));
    CD  += (ReD<=3.38E5 & ReD > 4.4E4).*((10).^(-4.3390+1.5809.*log10(ReD)-0.1546.*(log10(ReD).^2)));
    CD  += (ReD<=4E5 & ReD > 3.38E5).*(29.78-(5.3.*log10(ReD)));
    CD  += (ReD<=1E6 & ReD > 4E5).*(0.1.*log10(ReD)-0.49);
    CD  += (ReD>1E6).*(0.19-(8E4.*(ReD.^(-1))));
    CD(isnan(CD)) = 0;
endfunction

#- Função de ajuste da direção da Força de Arraste

function s=DA(v)
    s=zeros(1,3);
    s+=(v>=0)*-1;
    s+=(v<0);
endfunction

#- Funções Vetoriais

Par= @(h)(101325*(1-2.25577E-5*h)**5.25588);                              #[h] = m
Tar= @(h)(288.15-0.0065*(h));                                             #[h] = m
dAr= @(h)(Par(h)/(R*Tar(h)));                                             #[h] = m
Var= @(h)[(U0*(h/2E3)^(1/7))*sind(Theta) (U0*(h/2E3)^(1/7))*cosd(Theta) 0];
Rd = @(v,h)((dAr(h)*Desf*abs(v))/u);                                      #- Número de Reynolds
Fcd= @(v,h)((1/2)*gCD(Rd(v - Var(abs(h)),h))*dAr(h)*A.*((v - Var(abs(h))).^2));     #- Força de Arraste nas três direções
dV = @(v,h)(Fp + DA(v - Var(h)).*Fcd(v,h))/(Mesf);                        #- Aceleração na Esfera
dP = @(v)(v);                                                             #- Velocidade da Esfera

#-========= Runge-kutta Clássico de 4ª ordem =========-

delta  =        0.1;  # -> Tamanho do passo
tf     =         60;  # -> Tempo de Simulação
N      = (tf/delta);

v      = zeros(N,3);
p      = zeros(N,3);
v(1,:) =         V0;
p(1,:) =    [0 0 H];

i = 1;
while (i <= N)

  k1 = [dV(v(i,:),                      p(i,3))                     dP(v(i,:))];
  k2 = [dV(v(i,:)+(k1(1,1:3)*delta/2),  p(i,3)+(k1(1,6)*delta/2))   dP(v(i,:)+(k1(1,1:3)*delta/2))];
  k3 = [dV(v(i,:)+(k2(1,1:3)*delta/2),  p(i,3)+(k2(1,6)*delta/2))   dP(v(i,:)+(k2(1,1:3)*delta/2))];
  k4 = [dV(v(i,:)+(k3(1,1:3)*delta),    p(i,3)+(k3(1,6)*delta))     dP(v(i,:)+(k3(1,1:3)*delta))];

  v(i+1,:) = v(i,:) + ((k1(1,1:3)+2*(k2(1,1:3) + k3(1,1:3))+k4(1,1:3))*delta/6);
  p(i+1,:) = p(i,:) + ((k1(1,4:6)+2*(k2(1,4:6) + k3(1,4:6))+k4(1,4:6))*delta/6);

  if(p(i+1,3)<0)
    tf = i*delta; 
    p = resize(p,i+1,3);
    v = resize(v,i+1,3);
    p(i+1,3)= 0;
    break;
  endif
  if((i == N) && (p(i+1,3)>0))
    N += 10;
    tf = N*delta;
    p = resize(p,N+1,3);
    v = resize(v,N+1,3);
  endif
  i+=1;
endwhile

#-==== Plotagem dos gráficos
printf("A esfera atinge o chão em %0.2f segundos na seguinte posição (x,y) = (%0.3f,%0.3f).\n",tf,p(i,1),p(i,2));
if (abs(v(i,3)-v(i-1,3)-v(i-2,3))< 1E-2)
  printf("A esfera atinge a velocidade terminal. Vt = %0.2f",v(i,3));
else
  printf("A esfera não atingiu a velocidade terminal. =(");
endif
ti = 0:delta:tf;
figure(1,'numbertitle','off','name','Movimento Planar da Esfera');
clf;
  subplot(311);
    plot(ti,p(1:i+1,3));
    xlabel('t(s)');
    ylabel('h(m)');
    title('Trajetória da esfera - z');
  subplot(312);
    plot(ti,p(1:i+1,1));
    xlabel('t(s)');
    ylabel('x(m)');
    title('Trajetória da esfera - x');
  subplot(313); 
    plot(ti,p(1:i+1,2));
    ylabel('y(m)');
    xlabel('t(s)');
    title('Trajetória da esfera - x');
figure(2,'numbertitle','off','name','Movimento Tridimensional de Esfera');
clf;
  hold on;
  plot3(p(1:i,1),p(1:i,2),p(1:i,3),'linewidth',4);
  scatter3(p(i,1),p(i,2),p(i,3),'linewidth',12);

  zlabel('z(m)');
  ylabel('y(m)');
  xlabel('x(m)');
  grid on;
  view(3);
figure(3,'numbertitle','off','name','Movimento da Esfera No plano xy');
clf;
  plot(p(1:i+1,1),p(1:i+1,2));
  ylabel('y(m)');
  xlabel('x(m)');
