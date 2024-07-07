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
    new_object->string_value=NULL;
    new_object->value=0;
    new_object->rvalue=0;
    new_object->real_type=a;
    new_object->current_type=a;
    return new_object;
}

Object* object_bool(int a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=NULL;
    new_object->string_value=NULL;
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
    new_object->string_value=NULL;
    new_object->value=0;
    new_object->rvalue=a;
    new_object->real_type="Number";
    new_object->current_type="Number";
}

Object* object_Object(){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=NULL;
    new_object->string_value=NULL;
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
    if(a->rvalue != b->rvalue)return 0;
    if(a->value != b->value)return 0;
    if(strcmp(a->string_value,b->string_value))return 0;
    Node* cura=a->attributes->head;
    Node* curb=b->attributes->head;
    while(1){
        if(cura==NULL && curb==NULL)break;
        if(cura==NULL || curb==NULL)return 0;
        if(!equals(cura->value,curb->value))return 0;
        cura=cura->next;
        curb=curb->next;
    }
    return 1;
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

Object* function_rand(Object *a){
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

Object* object5_Range_next(Object* var_self){
    Object* mi=get(var_self->attributes,"current");
    mi=object_number(get_number(mi)+1);
    insert(var_self->attributes,"current",mi);
    if(get_number(mi)<get_number(get(var_self->attributes,"max"))){
        return object_bool(1);
    }else{
        return object_bool(0);
    }
}

Object* object5_Range_current(Object* var_self){
   return get(var_self->attributes,"current");
}

Object* function_range(Object* mi, Object* ma){
    return object_Range(mi,ma);
}


Object * Interface_1(Object * obj, Object * class, char * fun_name, Object * arg_0);
Object * Interface_0(Object * obj, Object * class, char * fun_name);
Object* object_Point(Object * Var_x, Object * Var_y);
Object * object5_Point_getX(Object * Var_self){
	{
		Object* Nod_5;
		Nod_5 = get((Var_self)->attributes, "Var_x");
		return Nod_5;
	}
}
Object * object5_Point_getY(Object * Var_self){
	{
		Object* Nod_7;
		Nod_7 = get((Var_self)->attributes, "Var_y");
		return Nod_7;
	}
}
Object * object5_Point_setX(Object * Var_self, Object * Arg_x){
	{
		Object * Var_x;
		Var_x = Arg_x;
		Object* Nod_9;
		Nod_9 = get((Var_self)->attributes, "Var_x");
		Object * Nod_10;
		Nod_10 = Var_x;
		( * Nod_9 ) = ( * Nod_10 );
		Object * Nod_11;
		Nod_11 = Nod_9;
		return Nod_11;
	}
}
Object * object5_Point_setY(Object * Var_self, Object * Arg_y){
	{
		Object * Var_y;
		Var_y = Arg_y;
		Object* Nod_13;
		Nod_13 = get((Var_self)->attributes, "Var_y");
		Object * Nod_14;
		Nod_14 = Var_y;
		( * Nod_13 ) = ( * Nod_14 );
		Object * Nod_15;
		Nod_15 = Nod_13;
		return Nod_15;
	}
}
Object* object_Point(Object * Var_x, Object * Var_y){
	Object* Var_self;
	Var_self = instantiate("Point");
	insert((Var_self)->attributes, "parent", object_Object());
	Object * Nod_1;
	Nod_1 = Var_x;
	Object * Nod_2;
	Nod_2 = Nod_1;
	insert((Var_self)->attributes, "Var_x", Nod_2);
	Object * Nod_3;
	Nod_3 = Var_y;
	Object * Nod_4;
	Nod_4 = Nod_3;
	insert((Var_self)->attributes, "Var_y", Nod_4);
	return Var_self;
}
Object * Interface_0(Object * obj, Object * class, char * fun_name){
	if(( (! strcmp("Range", (class)->real_type)) && (! strcmp("current", fun_name)) )){
		return object5_Range_current(obj);
	}
	if(( (! strcmp("Range", (class)->real_type)) && (! strcmp("next", fun_name)) )){
		return object5_Range_next(obj);
	}
	if(( (! strcmp("Point", (class)->real_type)) && (! strcmp("getX", fun_name)) )){
		return object5_Point_getX(obj);
	}
	if(( (! strcmp("Point", (class)->real_type)) && (! strcmp("getY", fun_name)) )){
		return object5_Point_getY(obj);
	}
	return Interface_0(obj, get((class)->attributes, "parent"), fun_name);
}
Object * Interface_1(Object * obj, Object * class, char * fun_name, Object * arg_0){
	if(( (! strcmp("Point", (class)->real_type)) && (! strcmp("setX", fun_name)) )){
		return object5_Point_setX(obj, arg_0);
	}
	if(( (! strcmp("Point", (class)->real_type)) && (! strcmp("setY", fun_name)) )){
		return object5_Point_setY(obj, arg_0);
	}
	return Interface_1(obj, get((class)->attributes, "parent"), fun_name, arg_0);
}
int main(){
	Object * Nod_34;
	{
		Object * Nod_17;
		Nod_17 = object_number(3);
		Object * Nod_18;
		Nod_18 = object_number(4);
		Object * Nod_19;
		Nod_19 = object_Point(Nod_17, Nod_18);
		Object * Nod_20;
		Nod_20 = Nod_19;
		Object * Var_pt;
		Var_pt = Nod_19;
		Object * Nod_21;
		Nod_21 = object_string("x: ");
		Object * Nod_22;
		Nod_22 = object_string("");
		Object * Nod_23;
		Nod_23 = Var_pt;
		Object * Nod_24;
		Nod_24 = Interface_0(Nod_23, Nod_23, "getX");
		Object * Nod_25;
		Nod_25 = concatenate(Nod_21, concatenate(Nod_22, Nod_24));
		Object * Nod_26;
		Nod_26 = object_string("");
		Object * Nod_27;
		Nod_27 = object_string("; y: ");
		Object * Nod_28;
		Nod_28 = concatenate(Nod_25, concatenate(Nod_26, Nod_27));
		Object * Nod_29;
		Nod_29 = object_string("");
		Object * Nod_30;
		Nod_30 = Var_pt;
		Object * Nod_31;
		Nod_31 = Interface_0(Nod_30, Nod_30, "getY");
		Object * Nod_32;
		Nod_32 = concatenate(Nod_28, concatenate(Nod_29, Nod_31));
		Object * Nod_33;
		Nod_33 = function_print(Nod_32);
		Nod_34 = Nod_20;
	}
	Object * Nod_35;
	Nod_35 = Nod_34;
	return 0;
}
