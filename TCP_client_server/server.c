#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>
#include<errno.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<netdb.h>
#include<arpa/inet.h>
#include<sys/wait.h>
#include<signal.h>
#define PORT "3490" //鎻愪緵缁欑敤鎴烽摼鎺ョ殑port
#define BACKLOG 10 //鏈夊灏戜釜pending connection queue

void sigchld_handler(int s)
{
	while (waitpid(-1, NULL, WNOHANG) > 0);
}

void *get_in_addr(struct sockaddr* sa)
{
	if (sa->sa_family == AF_INET) {
		return &(((struct sockaddr_in*)sa)->sin_addr);
	}
	else
		return &(((struct sockaddr_in6*)sa)->sin6_addr);
}

int main(void)
{
	int sockfd, new_fd; //鍦╯ockfd杩涜閾炬帴锛?new_fd鏄柊鐨勯摼鎺?
	struct addrinfo hints, *servinfo, *p;
	struct sockaddr_storage their_addr; //閾炬帴鑰呯殑鍦板潃璧勬枡
	socklen_t sin_size;
	struct sigaction sa;
	int yes = 1;
	char s[INET6_ADDRSTRLEN];
	int rv;

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_UNSPEC;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;

	if ((rv = getaddrinfo(NULL, PORT, &hints, &servinfo)) != 0) {
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv));
		return 1;
	}

	//浠ュ惊鐜壘鍑烘墍鏈夌殑缁撴灉锛?骞剁粦瀹?bind)鍒扮涓€涓兘鐢ㄧ殑缁撴灉
	for (p = servinfo; p != NULL; p = p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
			perror("server: socket");
			continue;
		}
		
		if (setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) == -1) {
			perror("setsockopt");
			exit(1);
		}

		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("server: bind");
			continue;
		}

		break;
	}

	if (p == NULL) {
		fprintf(stderr, "server: failed to bind\n");
		return 2;
	}

	freeaddrinfo(servinfo);
	
	if (listen(sockfd, BACKLOG) == -1) {
		perror("listen");
		exit(1);
	}

	sa.sa_handler = sigchld_handler; //鏀堕泦姝绘帀鐨刾rocess
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;

	if (sigaction(SIGCHLD, &sa, NULL) == -1) {
		perror("sigction");
		exit(1);
	}

	printf("server: waiting for connections..\n");

	while(1) { //涓昏鐨刟ccpet()寰幆
		sin_size = sizeof(their_addr);
		new_fd = accept(sockfd, (struct sockaddr*)&their_addr, &sin_size);

		if (new_fd == -1) {
			perror("accept");
			continue;
		}

		inet_ntop(their_addr.ss_family, get_in_addr((struct sockaddr *)&their_addr), s, sizeof(s));
		printf("server: got connection from %s\n", s);

		if (!fork()) {
			close(sockfd); //child process涓嶉渶瑕乴istener

			if (send(new_fd, "Hello, world!", 13, 0) == -1)
				perror("send");
			
			close(new_fd);

			exit(0);
		}
		close(new_fd); //parent涓嶉渶瑕佽繖涓?
	}
	return 0;
}
