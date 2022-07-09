void reactiondiffusion(void)
{
  int i,j,k,iup,idwn,jup,jdwn,kup,kdwn;
  double dphidx,dphidy;
  double d2phidxdx,d2phidydy;

  for(i=0;i<Lx;i++){
    if (i==Lx-1) iup=0; else iup=i+1;
    if (i==0) idwn=Lx-1; else idwn=i-1;
    for (j=0; j<Ly; j++) {
      if (j==Ly-1) jup=0; else jup=j+1;
      if (j==0) jdwn=Ly-1; else jdwn=j-1;

      dphidx=(phi[iup][j]-phi[idwn][j])/(2.0*dx);
      dphidy=(phi[i][jup]-phi[i][jdwn])/(2.0*dx);
	
      d2phidxdx=(phi[iup][j]+phi[idwn][j]-2.0*phi[i][j])/(dx*dx);
      d2phidydy=(phi[i][jup]+phi[i][jdwn]-2.0*phi[i][j])/(dx*dx);

      //update density here 

      phi_new[i][j]=phi[i][j]+dt*(D*(d2phidxdx+d2phidydy)-kappa*phi[i][j]+rho[i][j]);
      phi_new[i][j] -= dt*vx[j]*dphidx;

    }
  }
  
  for (i=0;i<Lx;i++){
    for (j=0;j<Ly;j++){
      phi[i][j]=phi_new[i][j];
    }
  }

}
 
  
