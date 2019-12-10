#include <cstdio>
#include <iostream>
#include <vector>
#include <set>
#include <map>
#include <algorithm>
#include <utility>
using namespace std;
#define X first
#define Y second
#define MP make_pair
typedef pair<long long,long long> pii ;
long long counter=0 ;
int n,m ;
class job
{
	public:
		vector <int> in_state ;
		int id ;
		long long in_time ;
	bool operator<(const job &a) const
	{
		if(in_time!= a.in_time)
			return in_time<a.in_time ;
		return id < a.id ;
	}
};
vector <job> all_jobs;

void input()
{
	cin>>n>>m ;
	for(int i=0;i<n;i++)
	{
		job new_job ;
		new_job.id=i ;
		cin>>new_job.in_time ;
		for(int i=0,v;i<m;i++)
		{
			cin>>v ;
			new_job.in_state.push_back(v) ;
		}
		all_jobs.push_back(new_job) ;
	}
}
int maxi_ans[100][100] ;
long long bruteforce_ans=(long long)1e15 ;
void bruteforce_do_job(int *arrange_stations)
{
    long long last_did[n+10] ;
    long long time[n+1][m+1] ;
    long long stations[m+1] ;
    for(int i=0;i<n*m;i++)
    {
        time[i/m][i%m]=0 ;
        stations[i%m]=0 ;
        last_did[i%n]=0 ;
    }
    for(int i=0;i<n*m;i++)
    {
        int job=arrange_stations[i]/m,workstation=arrange_stations[i]%m ;
        int mini=max(last_did[job],max(all_jobs[job].in_time,stations[workstation] ));
        time[job][workstation]=mini ;
        last_did[job]=mini+all_jobs[job].in_state[workstation] ;
        stations[workstation]=mini+all_jobs[job].in_state[workstation] ;
    }
    long long maxi=0 ;
    for(int i=0;i<m;i++)
        maxi=max(stations[i],maxi) ;
    if(bruteforce_ans>maxi)
    {
        cout<<maxi<<endl ;
        bruteforce_ans=maxi ;
        for(int i=0;i<n;i++)
            for(int j=0;j<m;j++)
                maxi_ans[i][j]=time[i][j] ;
    }
}
void bruteforce()
{
    int arrange_stations[10+n*m] ;
    for(int i=0;i<n*m;i++)
        arrange_stations[i]=i ;
    do {
            bruteforce_do_job(arrange_stations) ;
			counter++ ;
			if(counter%1000000==0)
				cout<<counter<<" round:\n" ;
    } while (next_permutation( arrange_stations,arrange_stations+n*m ));

}
int main()
{
    input();
    bruteforce() ;
    cout<<bruteforce_ans ;
}
