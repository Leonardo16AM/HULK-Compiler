#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

typedef struct Object Object;

// Estructura de nodo para la lista enlazada
typedef struct Node {
    char *key;
    Object *value;
    struct Node *next;
} Node;

// Estructura del mapa
typedef struct Map {
    Node *head;
} Map;

struct Object{
    char* real_type;
    char* current_type;
    Map* attributes;
    int value;
    float rvalue;
    char* string_value;
};

// Función para crear un nuevo nodo
Node *createNode(char *key, Object *value) {
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Error: no se pudo asignar memoria para el Nodo");
        exit(1);
    }
    newNode->key = strdup(key); // Copiar la clave
    newNode->value = value; // Copiar la referencia
    newNode->next = NULL;
    return newNode;
}

// Función para crear un mapa vacío
Map *createMap() {
    Map *newMap = (Map *)malloc(sizeof(Map));
    if (newMap == NULL) {
        printf("Error: no se pudo asignar memoria para el Mapa");
        exit(1);
    }
    newMap->head = NULL;
    return newMap;
}

Object *real_get(Map *map, char *key) {
    Node *current = map->head;
    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            return current->value;
        }
        current = current->next;
    }
    return NULL;
}

// Función para buscar un valor por clave
Object *get(Map *map, char *key) {
    Node *current = map->head;
    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            return current->value;
        }
        current = current->next;
    }
    Object* par= real_get(map,"parent");
    if(par==NULL)return NULL;
    if(par->attributes==NULL)return NULL;
    return get(par->attributes,key);
}

// Función para insertar un par clave-valor en el mapa
void insert(Map *map, char *key, Object *value) {
    Object* F;
    if(key=="parent"){
        F= real_get(map,key);
    }else{
        F= get(map, key);
    }
    if(F!=NULL){
        *F=*value;
        return;
    }
    Node *newNode = createNode(key, value);
    newNode->next = map->head;
    map->head = newNode;
}

// Función para eliminar un par clave-valor del mapa
void removeKey(Map *map, char *key) {
    Node *current = map->head;
    Node *previous = NULL;

    while (current != NULL) {
        if (strcmp(current->key, key) == 0) {
            if (previous == NULL) {
                map->head = current->next;
            } else {
                previous->next = current->next;
            }
            free(current->key);
            free(current->value);
            free(current);
            return;
        }
        previous = current;
        current = current->next;
    }
}

// Función para liberar la memoria del mapa
void destroyMap(Map *map) {
    Node *current = map->head;
    while (current != NULL) {
        Node *next = current->next;
        free(current->key);
        free(current->value);
        free(current);
        current = next;
    }
    free(map);
}





// Nodo de la lista enlazada
typedef struct SetNode {
    char *data;
    struct SetNode *next;
} SetNode;

// Estructura del set
typedef struct StringSet {
    SetNode *head;
} StringSet;

// Función para crear un nuevo nodo
SetNode *createSetNode(char *data) {
    SetNode *newNode = (SetNode *)malloc(sizeof(Node));
    if (newNode == NULL) {
        printf("Error: no se pudo asignar memoria para el nodo.n");
        exit(1);
    }
    newNode->data = strdup(data);
    newNode->next = NULL;
    return newNode;
}

// Función para crear un set vacío
StringSet *createStringSet() {
    StringSet *newSet = (StringSet *)malloc(sizeof(StringSet));
    if (newSet == NULL) {
        printf("Error: no se pudo asignar memoria para el set.n");
        exit(1);
    }
    newSet->head = NULL;
    return newSet;
}

// Función para verificar si un elemento está presente en el set
int contains(StringSet *set, char *data) {
    SetNode *current = set->head;
    while (current != NULL) {
        if (strcmp(current->data, data) == 0) {
            return 1;
        }
        current = current->next;
    }
    return 0;
}

// Función para insertar un elemento en el set
void Set_insert(StringSet *set, char *data) {
    // Si el elemento ya existe, no se hace nada
    if (contains(set, data)) {
        return;
    }

    SetNode *newNode = createSetNode(data);
    newNode->next = set->head;
    set->head = newNode;
}

// Función para eliminar un elemento del set
void removeElement(StringSet *set, char *data) {
    SetNode *current = set->head;
    SetNode *previous = NULL;

    while (current != NULL) {
        if (strcmp(current->data, data) == 0) {
            if (previous == NULL) {
                set->head = current->next;
            } else {
                previous->next = current->next;
            }
            free(current->data);
            free(current);
            return;
        }
        previous = current;
        current = current->next;
    }
}

// Función para liberar la memoria del set
void destroyStringSet(StringSet *set) {
    SetNode *current = set->head;
    while (current != NULL) {
        SetNode *next = current->next;
        free(current->data);
        free(current);
        current = next;
    }
    free(set);
}




typedef struct Class{
    char* Name;
    struct Class *Parent;
} Class;







Object* instantiate(char* a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=createMap();
    new_object->string_value="";
    new_object->value=0;
    new_object->rvalue=0;
    new_object->real_type=a;
    new_object->current_type=a;
    return new_object;
}

Object* object_bool(int a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=NULL;
    new_object->string_value="";
    new_object->value=a;
    new_object->rvalue=0;
    new_object->real_type="Boolean";
    new_object->current_type="Boolean";
}

Object* object_string(char* a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=NULL;
    new_object->string_value=a;
    new_object->value=0;
    new_object->rvalue=0;
    new_object->real_type="String";
    new_object->current_type="String";
}

Object* object_number(float a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=NULL;
    new_object->string_value="";
    new_object->value=0;
    new_object->rvalue=a;
    new_object->real_type="Number";
    new_object->current_type="Number";
}

Object* object_Object(){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=NULL;
    new_object->string_value="";
    new_object->value=0;
    new_object->rvalue=0;
    new_object->real_type="Object";
    new_object->current_type="Object";
}

int get_bool(Object* a){
    return a->value;
}

float get_number(Object* a){
    return a->rvalue;
}

float modulo(float a , float b){
    float s=a;
    float m=b;
    int is=s+0.5;
    int im=m+0.5;
    int id=is%im;
    float d=id;
    return d;
}


char* get_string(Object *a){
    
    if(a->real_type=="String"){
        return a->string_value;
    }
    if(a->real_type=="Number"){
        char* cadena=(char*)malloc(20);
        snprintf(cadena,sizeof(cadena),"%f",a->rvalue);
        return cadena;
    }
    if(a->real_type=="Boolean"){
        if(a->value==0){
            return "false";
        }else{
            return "true";
        }
    }
    char* f="instance of ";
    int d=strlen(a->current_type);
    char* ans=(char*)malloc(d+50);
    snprintf(ans,d+50, "%s%s",f,ans);
    return ans;
}

Object *concatenate(Object* a,Object* b){
    char *sa=get_string(a);
    char *sb=get_string(b);
    int len=strlen(sa)+strlen(sb)+3;
    char* ans=(char*)malloc(len);
    snprintf(ans,len,"%s%s",sa,sb);
    return object_string(ans);
}

Object* is_child_from_class(Object* a,char* type){
    if(a->real_type==type)return object_bool(1);
    if(a->real_type=="Object")return object_bool(0);
    return is_child_from_class(get(a->attributes,"parent"),type);
}

int equals(Object *a,Object *b){
    if(a->real_type != b->real_type)return 0;
    if(a->rvalue - b->rvalue>1e-7 || a->rvalue - b->rvalue<-1e-7)return 0;
    if(a->value != b->value)return 0;
    if(strcmp(a->string_value,b->string_value))return 0;
    printf("F");
    if(a->attributes==NULL && b->attributes==NULL)return 1;
    if(a->attributes!=NULL && b->attributes!=NULL){
    Node* cura=a->attributes->head;
    Node* curb=b->attributes->head;
    while(1){
        if(cura==NULL && curb==NULL)break;
        if(cura==NULL || curb==NULL)return 0;
        if(!equals(cura->value,curb->value))return 0;
        cura=cura->next;
        curb=curb->next;
    }
    }else{
        return 0;
    }
    return 1;
}

#define Var_PI object_number(acos(-1))
#define Var_E object_number(exp(1))

Object* copy(Object* a){
    Object* b=(Object*)(malloc(sizeof(Object*)));
    b->real_type=a->real_type;
    b->rvalue=a->rvalue;
    b->value=a->value;
    strcpy(b->string_value,a->string_value);
    b->attributes=createMap();
    Node* cura=a->attributes->head;
    while(1){
        if(cura==NULL)break;
        insert(b->attributes,cura->key,copy(cura->value));
        cura=cura->next;
    }
    return b;
}

Object* function_print(Object *a){
    printf("%s\n",get_string(a));
    return a;
}

Object* function_sqrt(Object *a){
    return object_number(sqrtf(get_number(a)));
}

Object* function_sin(Object *a){
    return object_number(sin(get_number(a)));
}

Object* function_cos(Object *a){
    return object_number(cos(get_number(a)));
}

Object* function_exp(Object *a){
    return object_number(exp(get_number(a)));
}

Object* function_log(Object *bas,Object* arg){
    return object_number(log(get_number(arg))/log(get_number(bas)));
}

Object* function_rand(){
    return object_number((double)rand() / (double)RAND_MAX);
}

Object* object_Range(Object* min, Object* max){
    Object *self=instantiate("Range");
    insert(self->attributes,"parent",object_Object());
    insert(self->attributes,"min",min);
    insert(self->attributes,"max",max);
    insert(self->attributes,"current",object_number(get_number(min)-1));
    return self;
}

Object* object5_Range_next(Object* Var_self){
    Object* mi=get(Var_self->attributes,"current");
    mi=object_number(get_number(mi)+1);
    insert(Var_self->attributes,"current",mi);
    if(get_number(mi)<get_number(get(Var_self->attributes,"max"))){
        return object_bool(1);
    }else{
        return object_bool(0);
    }
}

Object* object5_Range_reset(Object* Var_self){
    Object* mi=get(Var_self->attributes,"min");
    mi=object_number(get_number(mi)-1);
    insert(Var_self->attributes,"current",mi);
    return mi;
}

Object* object5_Range_current(Object* Var_self){
   return get(Var_self->attributes,"current");
}

Object* object_let(){
    Object *self=instantiate("let");
    insert(self->attributes,"parent",object_Object());
    insert(self->attributes,"size",object_bool(0));
    insert(self->attributes,"current",object_number(0));
    return self;
}

Object* object3_let_next(Object* Var_self){
    Object* mi=get(Var_self->attributes,"current");
    mi=object_number(get_number(mi)+1);
    insert(Var_self->attributes,"current",mi);
    if(get_number(mi)<get_bool(get(Var_self->attributes,"size"))){
        return object_bool(1);
    }else{
        return object_bool(0);
    }
}

Object* object3_let_current(Object* Var_self){
   Object* meg=get(Var_self->attributes,"current");
   int d=get_number(meg)+0.0000001;
   char* f=(char*)malloc(33);
    snprintf(f,33,"%d",d);
    return get(Var_self->attributes,f);
}

Object* object3_let_reset(Object* Var_self){
    Object* mi=object_number(-1);
    insert(Var_self->attributes,"current",mi);
    return mi;
}

Object* object3_let_append(Object* Var_self,Object* value){
    Object* mi=get(Var_self->attributes,"size");
    char* f=(char*)malloc(33);
    snprintf(f,33,"%d",get_bool(mi));
    insert(Var_self->attributes,f,value);
    insert(Var_self->attributes,"size",object_bool(get_bool(mi)+1));
    return value;
}

Object* object3_let_index(Object* Var_self,Object* index){
    char* f=(char*)malloc(33);
    snprintf(f,33,"%d",(int)(get_number(index)+1e-6));
    return  get(Var_self->attributes,f);
}

Object* object3_let_size(Object* Var_self){
    return  object_number( get_bool(get(Var_self->attributes,"size")));
}

Object* object6_string_index(Object* Var_self,Object* index){
    int d=(int)(get_number(index)+1e-6);
    char c=*(Var_self->string_value+d);
    char* f=(char*)malloc(2);
    snprintf(f,2,"%c",c);
    return  object_string(f);
}

Object* object6_string_size(Object* Var_self){
    return  object_number(strlen(Var_self->string_value));
}

Object* function_range(Object* mi, Object* ma){
    return object_Range(mi,ma);
}



//Finish C_TOOLS

int main() {
    Map *myMap = createMap();
    insert(myMap, "nombre", "Juan");
    insert(myMap, "edad", "30");
    insert(myMap, "ciudad", "Madrid");

    printf("Valor de 'nombre': %sn", get(myMap, "nombre"));
    printf("Valor de 'edad': %sn", get(myMap, "edad"));
    printf("Valor de 'ciudad': %sn", get(myMap, "ciudad"));

    removeKey(myMap, "edad");
    printf("Valor de 'edad': %sn", get(myMap, "edad"));

    destroyMap(myMap);

    return 0;
}
