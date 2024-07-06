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


Object * Interface_0(Object * obj, Object * class, char * fun_name);
Object* object_Person(Object * Var_first, Object * Var_last);
Object* object_Knight(Object * Var_firstname, Object * Var_lastname);
Object * object6_Knight_name(Object * Var_self){
	{
		Object * Nod_3;
		Nod_3 = object_string("Sir");
		Object * Nod_4;
		Nod_4 = object_string(" ");
		Object * Nod_5;
		Nod_5 = Interface_0(get((Var_self)->attributes, "parent"), get((Var_self)->attributes, "parent"), "name");
		Object * Nod_6;
		Nod_6 = concatenate(Nod_3, concatenate(Nod_4, Nod_5));
		return Nod_6;
	}
}
Object * object6_Knight_wacala(Object * Var_self){
	{
		Object * Nod_8;
		Nod_8 = Var_self;
		Object * Nod_9;
		Nod_9 = Interface_0(Nod_8, Nod_8, "say_my_name");
		Object * Nod_10;
		Nod_10 = Nod_9;
		return Nod_10;
	}
}
Object* object_Knight(Object * Var_firstname, Object * Var_lastname){
	Object* Var_self;
	Var_self = instantiate("Knight");
	Object * Nod_1;
	Nod_1 = Var_firstname;
	Object * Nod_2;
	Nod_2 = Var_lastname;
	insert((Var_self)->attributes, "parent", object_Person(Nod_1, Nod_2));
	return Var_self;
}
Object * object6_Person_say_my_name(Object * Var_self){
	{
		Object * Nod_16;
		Nod_16 = Var_self;
		Object * Nod_17;
		Nod_17 = Interface_0(Nod_16, Nod_16, "name");
		Object * Nod_18;
		Nod_18 = function_print(Nod_17);
		Object * Nod_19;
		Nod_19 = Nod_18;
		return Nod_19;
	}
}
Object * object6_Person_name(Object * Var_self){
	{
		Object* Nod_21;
		Nod_21 = get((Var_self)->attributes, "Var_firstname");
		Object * Nod_22;
		Nod_22 = object_string(" ");
		Object* Nod_23;
		Nod_23 = get((Var_self)->attributes, "Var_lastname");
		Object * Nod_24;
		Nod_24 = concatenate(Nod_21, concatenate(Nod_22, Nod_23));
		return Nod_24;
	}
}
Object * object6_Person_hash(Object * Var_self){
	{
		Object * Nod_26;
		Nod_26 = object_number(5);
		Object * Nod_27;
		Nod_27 = Nod_26;
		return Nod_27;
	}
}
Object* object_Person(Object * Var_first, Object * Var_last){
	Object* Var_self;
	Var_self = instantiate("Person");
	insert((Var_self)->attributes, "parent", object_Object());
	Object * Nod_12;
	Nod_12 = Var_first;
	Object * Nod_13;
	Nod_13 = Nod_12;
	insert((Var_self)->attributes, "Var_firstname", Nod_13);
	Object * Nod_14;
	Nod_14 = Var_last;
	Object * Nod_15;
	Nod_15 = Nod_14;
	insert((Var_self)->attributes, "Var_lastname", Nod_15);
	return Var_self;
}
Object * Interface_0(Object * obj, Object * class, char * fun_name){
	if(( (! strcmp("Range", (class)->real_type)) && (! strcmp("current", fun_name)) )){
		return object5_Range_current(obj);
	}
	if(( (! strcmp("Range", (class)->real_type)) && (! strcmp("next", fun_name)) )){
		return object5_Range_next(obj);
	}
	if(( (! strcmp("Knight", (class)->real_type)) && (! strcmp("name", fun_name)) )){
		return object6_Knight_name(obj);
	}
	if(( (! strcmp("Knight", (class)->real_type)) && (! strcmp("wacala", fun_name)) )){
		return object6_Knight_wacala(obj);
	}
	if(( (! strcmp("Person", (class)->real_type)) && (! strcmp("say_my_name", fun_name)) )){
		return object6_Person_say_my_name(obj);
	}
	if(( (! strcmp("Person", (class)->real_type)) && (! strcmp("name", fun_name)) )){
		return object6_Person_name(obj);
	}
	if(( (! strcmp("Person", (class)->real_type)) && (! strcmp("hash", fun_name)) )){
		return object6_Person_hash(obj);
	}
	return Interface_0(obj, get((class)->attributes, "parent"), fun_name);
}
int main(){
	Object * Nod_36;
	{
		Object * Nod_29;
		Nod_29 = object_string("Edian");
		Object * Nod_30;
		Nod_30 = object_string("Broche \n Castro");
		Object * Nod_31;
		Nod_31 = object_Knight(Nod_29, Nod_30);
		Object * Nod_32;
		Nod_32 = Nod_31;
		Object * Var_leo;
		Var_leo = Nod_31;
		Object * Nod_33;
		Nod_33 = Var_leo;
		Object * Nod_34;
		Nod_34 = Interface_0(Nod_33, Nod_33, "say_my_name");
		Object * Nod_35;
		Nod_35 = Nod_34;
		Nod_36 = Nod_32;
	}
	Object * Nod_37;
	Nod_37 = Nod_36;
	return 0;
}
