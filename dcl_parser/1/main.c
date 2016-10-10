#include<stdio.h>
#include<string.h>
#include<ctype.h>
#include"get.c"

#define MAXTOKEN 100

enum { NAME, PARENS, BRACKETS };
enum { NO, YES };


int tokentype; //×îºóÒ»¸ö¼ÇºÅµÄÀàÐÍ
char token[MAXTOKEN]; //×îºóÒ»¸ö¼ÇºÅ×Ö·û´® 
char name[MAXTOKEN]; //±êÊ¶·ûÃû 
char datatype[MAXTOKEN];  //Êý¾ÝÀàÐÍÎªchar¡¢ intµÈ 
char out[1000]; //Êä³ö´® 
int prevtoken = NO;

void dcl(void);
void dirdcl(void);
void errmsg(char *);
int gettoken(void);

int main()
{
	while (gettoken() != EOF) {
		strcpy(datatype, token);
		out[0] = '\0';
		dcl();
		if (tokentype != '\n')
		    printf("syntax error\n");
        if (tokentype == '(') printf("you meet (");
        printf("%s: %s %s\n", name, out, datatype);
	}
	return 0;
}

int gettoken(void) //token: (); [number]; NAME; singel character.  
{
	int c, getch(void);
	void ungetch(int);
	char *p = token;

	if (prevtoken == YES) {
		prevtoken = NO;
		printf("\npretoken tokentype in ascii: %d \n", tokentype);
		return tokentype;
	}
	while ((c = getch()) == ' ' || c == '\t')
	    ;
    if (c == '(') {
    	if ((c = getch()) == ')') {
    		strcpy(token, "()");
    		return tokentype = PARENS;
    	}
    	else {
    		ungetch(c);
    		return tokentype = '(';
    	}
    }
    else if (c == '[') {
    	for (*p++ = c; (*p++ = getch()) != ']'; )
    	    ;
	    *p = '\0';
	    return tokentype = BRACKETS;
    }
    else if (isalpha(c)) {
    	for (*p++ = c; isalnum(c = getch()); )
    	    *p++ = c;
	    *p = '\0';
	    ungetch(c);
	    return tokentype = NAME;
    }
    else
        return tokentype = c;
}



void dcl(void)
{
	int ns;
	for (ns = 0; gettoken() == '*'; ) //ÊÕ¼¯ÈÎÒâÊýÁ¿µÄ* 
	    ns++;
    dirdcl();
    while (ns-- > 0)
        strcat(out, " pointer to");
} 

void dirdcl(void)
{
	int type;
	if (tokentype == '(') {         // ( dcl ) 
		dcl();
		if (tokentype != ')')
		    errmsg("error: missing )\n");
	}
	else if (tokentype == NAME)   //±äÁ¿Ãû×Ö 	
	    strcpy(name, token);
    else
        errmsg("error: expected name or (dcl)\n");
        
    while ((type=gettoken()) == PARENS || type == BRACKETS)
        if (type == PARENS)
            strcat(out, " function returning");
        else {
        	strcat(out, " array");
        	strcat(out, token);
        	strcat(out, " of");
        }
}

void errmsg(char *msg)
{
	printf("%s", msg);
	prevtoken = YES;
}
