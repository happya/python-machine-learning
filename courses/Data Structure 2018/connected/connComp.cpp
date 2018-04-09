/*
 * connComp.cpp
 *
 *  Created on: 2018Äê4ÔÂ8ÈÕ
 *      Author: yyiust
 */


#include <iostream>
#include <cstdio>
#include <queue>
#define MaxN 10
using namespace std;


int G[MaxN][MaxN]={0};
int visited1[MaxN]={0};
int visited2[MaxN]={0};
int result[MaxN];
int N,E,k;

void BFS(int v);
void DFS(int v);

int main(){

	cin>>N>>E;

	int u,v;
	for(int i=0;i<E;i++){
		cin>>u>>v;
		G[u][v]=G[v][u]=1;
	}

	for (int i=0;i<N;i++){
		k = 0;
		if (visited1[i]==0){
			DFS(i);
			cout<<"{ ";
			for (int j=0;j<k;j++)
				cout<<result[j]<<' ';
			cout<<"}"<<endl;
		}

	}


	for (int i=0;i<N;i++){
		k = 0;
		if (visited2[i]==0){
			BFS(i);
			cout<<"{ ";
			for (int j=0;j<k;j++)
				cout<<result[j]<<' ';
			cout<<"}"<<endl;
		}
	}

	return 0;
}

void DFS(int v){
	visited1[v]=1;
	result[k++]=v;
	for (int i=0;i<N;i++){
		if (G[v][i]==1 && visited1[i]==0)
			DFS(i);

	}
}

void BFS(int v){
	queue<int> q;
	q.push(v);
	visited2[v]=1;
	result[k++]=v;
	while(!q.empty()){
		int u = q.front();
		q.pop();
		for(int i=0;i<N;i++){
			if (G[u][i]!=0 && visited2[i]!=1){
				visited2[i]=1;
				q.push(i);
				result[k++]=i;
			}
		}
	}
}


