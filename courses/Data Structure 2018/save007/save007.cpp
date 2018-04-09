/*
 * save007.cpp
 *
 *  Created on: 2018Äê4ÔÂ8ÈÕ
 *      Author: yyiust
 */


#include <iostream>
#include <cstdio>
#include <math.h>
#define MaxN 100
#define MinLen 42.5
using namespace std;

struct coordinate{
	int x;
	int y;
}P[MaxN];

int N,MaxD,MaxD2;
bool flag;

bool visited[MaxN]={false};
bool canJump(int p1,int p2);
bool DFS(int v);


int main(){
	cin>>N>>MaxD;
	MaxD2 = MaxD*MaxD;
	for (int i=0;i<N;i++){
		cin>>P[i].x;
		cin>>P[i].y;
	}
	if (MaxD>MinLen)
		cout<<"Yes"<<endl;
	else{
		for (int i=0;i<N;i++){
			int d2 = pow(P[i].x,2)+pow(P[i].y,2);
			if (d2<=(MaxD+7.5)*(MaxD+7.5) && !visited[i]){
				if (DFS(i)){

					break;
				}
			}

		}
		if (flag)
			cout<<"Yes"<<endl;
		else
			cout<<"No"<<endl;
	}
	return 0;
}


bool canJump(int p1,int p2){
	int x2 = pow(P[p1].x-P[p2].x,2);
	int y2 = pow(P[p1].y-P[p2].y,2);
	if (x2+y2>MaxD2)
		return false;
	return true;
}

bool isSafe(int p){
	int x0 = P[p].x;
	int y0 = P[p].y;
	if ( (50-x0)<=MaxD || (50-y0)<=MaxD || (50+x0)<=MaxD || (50+y0)<=MaxD )
		return true;
	return false;
}


bool DFS(int v){
	visited[v]=true;
	if (isSafe(v))
		flag = true;

	for (int i=0;i<N;i++){
		if (!visited[i] && canJump(v,i)){
			flag = DFS(i);
			if (flag)
				return true;
		}
	}
	return flag;
}
