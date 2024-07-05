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

// Función para insertar un par clave-valor en el mapa
void insert(Map *map, char *key, Object *value) {
    Node *newNode = createNode(key, value);
    newNode->next = map->head;
    map->head = newNode;
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
    return NULL; // Clave no encontrada
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





struct Object{
    char* real_type;
    char* current_type;
    Map* attributes;
    int value;
    float rvalue;
    char* string_value;
};

Object* instantiate(char* a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->attributes=createMap();
    new_object->real_type=a;
    new_object->current_type=a;
    return new_object;
}

Object* object_bool(int a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->value=a;
    new_object->real_type="Boolean";
    new_object->current_type="Boolean";
}

Object* object_string(char* a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->string_value=a;
    new_object->real_type="String";
    new_object->current_type="String";
}

Object* object_number(float a){
    Object *new_object = (Object* )malloc(sizeof(Object));
    new_object->rvalue=a;
    new_object->real_type="Number";
    new_object->current_type="Number";
}

Object* object_Object(){
    Object *new_object = (Object* )malloc(sizeof(Object));
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
