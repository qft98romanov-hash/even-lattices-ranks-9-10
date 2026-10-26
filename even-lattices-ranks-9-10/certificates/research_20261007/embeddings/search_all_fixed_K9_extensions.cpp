// Exhaustive integer relaxation of an exactly certified rational ellipsoid.
// No floating-point quantity is used to prune a branch. sqrt() only proposes
// a square-root integer, corrected by exact integer comparisons before use.
#include <iostream>
#include <cmath>
#include <cstdint>
#include <cassert>
#include <algorithm>
using namespace std;
using u128=__uint128_t;using i128=__int128_t;using i64=int64_t;using u64=uint64_t;
int n,caseid; i64 S,wn,df[50],yr[50],E[50],B[50],g[50],mu[50][50],C[50][50],x[50];u64 nodes=0,leaves=0,found=0;u128 limit;
u64 isqrt(u64 q){u64 r=(u64)sqrt((long double)q);while((u128)(r+1)*(r+1)<=q)++r;while((u128)r*r>q)--r;return r;}
i64 floordiv(i64 a,i64 b){i64 q=a/b,r=a%b;return q-(r<0);}
i64 ceildiv(i64 a,i64 b){return -floordiv(-a,b);}
void dfs(int k,u128 rem){
 ++nodes;
 if(k<0){
  ++leaves;i128 v=wn;for(int i=0;i<n;i++){v+=2*(i128)x[i]*g[i];for(int j=0;j<n;j++)v+=(i128)x[i]*C[i][j]*x[j];}
  assert(v>=6);if(v==6){++found;cout<<"EXACT_NORM6_WITNESS "<<caseid<<' ';for(int i=0;i<n;i++)cout<<x[i]<<' ';cout<<endl;}return;
 }
 i128 cc=yr[k];for(int j=k+1;j<n;j++)cc-=(i128)x[j]*mu[j][k];assert(cc>INT64_MIN&&cc<INT64_MAX);i64 c=(i64)cc;
 u128 div=rem/df[k];assert(div<=UINT64_MAX);i64 rad=(i64)isqrt((u64)div)+E[k];
 i64 lo=max(-B[k],ceildiv(c-rad,S)),hi=min(B[k],floordiv(c+rad,S));
 if(lo>hi)return;
 i64 nearest=floordiv(c+S/2,S);nearest=max(lo,min(hi,nearest));
 for(i64 t=0;t<=max(nearest-lo,hi-nearest);t++){
  for(int ss=0;ss<(t?2:1);ss++){
   i64 v=nearest+(ss? -t:t);if(v<lo||v>hi)continue;
   i64 a=max<i64>(0,(i64)llabs(S*v-c)-E[k]);u128 term=(u128)a*a*df[k];
   if(term<=rem){x[k]=v;dfs(k-1,rem-term);}
  }
 }
}
int main(){
 int cases;cin>>n>>S>>cases;assert(n>0&&n<50&&S>0);
 for(int i=0;i<n;i++)cin>>df[i];
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)cin>>mu[i][j];
 for(int i=0;i<n;i++)for(int j=0;j<n;j++)cin>>C[i][j];
 limit=(u128)5*S*S*S/2;
 for(caseid=0;caseid<cases;caseid++){
  cin>>wn;for(auto a:{yr,E,B,g})for(int i=0;i<n;i++)cin>>a[i];
  for(int i=0;i<n;i++)assert(df[i]>0&&B[i]>=0&&E[i]>=0);
  nodes=leaves=found=0;dfs(n-1,limit);
  cout<<"CASE "<<caseid<<" NODES "<<nodes<<" LEAVES "<<leaves<<" NORM6_WITNESSES "<<found<<endl;
 }
 cout<<"ALL_FIXED_K9_FIBERS_COMPLETED "<<cases<<endl;
}
