/*
 * ufind.cpp
 *
 *  Created on: 2018Äê4ÔÂ2ÈÕ
 *      Author: yyiust
 */

#include<iostream>
#include <stdlib.h>
using namespace std;

int find(int x,int root[]);
bool check(int x,int y,int root[],int rank[]);
void uni(int x,int y,int root[],int rank[]);

int main(){
	int N,node1,node2;
	char state;
	cin>>N;
	int root[N+1];
	int rank[N+1];
	for(int i=1;i<=N;i++)
		root[i] = i;
	while(cin>>state){
		if (state!='S'){
		cin>>node1>>node2;
		if (state=='C'){
			if (check(node1,node2,root,rank))
					cout<<"yes"<<endl;
			else
				cout<<"no"<<endl;
			continue;
		}
		if (state=='I'){
			uni(node1,node2,root,rank);
			continue;
		}

	}
		else break;
	}

	int count = 1;
	for(int i=1;i<=N;i++){
		root[i] = find(i,root);
	}

	int cur = root[1];
	for(int i=2;i<=N;i++){
		if (root[i]!=cur)
			count++;
		cur = root[i];
	}
	if(count==1)
		cout<<"The network is connected."<<endl;
	else
		cout<<"There are "<<count<<" components."<<endl;
	return 0;
}

int find(int x,int root[]){
	if (root[x]!=x)
		root[x]=find(root[x],root);
	return root[x];
}

bool check(int x,int y,int root[],int rank[]){
	int xr = find(x,root);
	int yr = find(y,root);
	if (xr==yr)
		return true;
	else
		return false;
}

void uni(int x,int y,int root[],int rank[]){
	int xr = find(x,root);
	int yr = find(y,root);
	if (xr==yr)
		return;
	else if (rank[xr]>rank[yr]) root[yr]=xr;
	else if (rank[xr]<rank[yr]) root[xr]=yr;
	else{
		root[yr]=xr;
		rank[xr]++;
	}
	return;
}
