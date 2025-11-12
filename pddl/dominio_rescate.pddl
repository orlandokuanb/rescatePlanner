;; =============================================================================
;; DOMINIO PDDL - RESCATE EN MINA CON CONSTRUCCIÓN DE INFRAESTRUCTURA
;; Curso: MIA-103 Fundamentos de Inteligencia Artificial
;; Problema: Planificación automatizada de rescate con obstáculos
;; =============================================================================

(define (domain rescate-mina)
    
    ;; =========================================================================
    ;; REQUIREMENTS
    ;; =========================================================================
    (:requirements 
        :strips                     ; Acciones básicas con precondiciones y efectos
        :typing                     ; Sistema de tipos
        :negative-preconditions     ; Permite (not ...) en precondiciones
        :equality                   ; Permite comparaciones con =
    )
    
    ;; =========================================================================
    ;; TIPOS (Jerarquía de conceptos del dominio)
    ;; =========================================================================
    (:types 
        locacion recurso - object
        
        ; Tipos de recursos
        infraestructura maquinaria suministro - recurso
        puente carretera - infraestructura
        
        ; Unidades móviles
        unidad_movil - object
        
        ; Personas (jerarquía completa)
        persona - object
        personal_rescate personal_construccion victima conductor - persona
        
        ; Subtipos de personal de rescate
        medico rescatista asistente - personal_rescate
        
        ; Subtipos de personal de construcción  
        tecnico obrero ingeniero operador - personal_construccion
        
        ; Subtipos de víctimas (según gravedad)
        victima_grave victima_estable victima_no_afectada - victima
    )
    
    ;; =========================================================================
    ;; PREDICADOS (Relaciones y propiedades del dominio)
    ;; =========================================================================
    (:predicates
        ;; --- RELACIONES ESPACIALES ---
        (en ?e - object ?l - locacion)
        ; Entidad e está físicamente en locación l
        
        (adyacente ?l1 ?l2 - locacion)
        ; Locaciones l1 y l2 son consecutivas en la ruta
        
        (conecta ?i - infraestructura ?l1 ?l2 - locacion)
        ; Infraestructura i permite cruzar de l1 a l2
        
        ;; --- RELACIONES DE TRANSPORTE ---
        (dentro ?p - persona ?u - unidad_movil)
        ; Persona p está siendo transportada en unidad u
        
        (carga ?r - recurso ?u - unidad_movil)
        ; Recurso r está cargado en unidad u
        
        (puede_transportar_carga ?u - unidad_movil)
        ; Unidad u tiene capacidad para transportar recursos pesados
        
        (espacio_disponible ?u - unidad_movil)
        ; Unidad u tiene al menos un espacio libre
        
        (vacia ?u - unidad_movil)
        ; Unidad u no tiene personas ni carga
        
        ;; --- ESTADO DE INFRAESTRUCTURA ---
        (construido ?i - infraestructura)
        ; Infraestructura i ha sido construida
        
        (operativo ?i - infraestructura)
        ; Infraestructura i está operativa y puede usarse
        
        (tarea_completada ?i - infraestructura)
        ; Tarea de construcción completada, personal puede regresar
        
        ;; --- ESTADO DE VÍCTIMAS ---
        (estabilizado ?v - victima_grave)
        ; Víctima grave v ha sido estabilizada por el médico
        
        (rescatado ?v - victima)
        ; Víctima v ha llegado exitosamente a la base
        
        (requiere_estabilizacion ?v - victima)
        ; Víctima v necesita atención médica urgente
        
        ;; --- CONTROL DE FLUJO ---
        (puede_avanzar_a ?l - locacion)
        ; Se permite avanzar a locación l (infraestructura previa lista)
        
        (disponible ?p - persona)
        ; Persona p no está dentro de ninguna unidad
        
        (asignado_a_tarea ?op - operador ?l - locacion)
        ; Operador op está asignado a mantener infraestructura en l
        
        ;; --- CLASIFICACIÓN DE LOCACIONES ---
        (base ?l - locacion)
        ; Locación l es la base de operaciones (C0)
        
        (zona_estacionamiento ?l - locacion)
        ; Locación l tiene área de estacionamiento
        
        (zona_desastre ?l - locacion)
        ; Locación l es donde están las víctimas (M)
        
        ;; --- CAPACIDADES ESPECÍFICAS ---
        (puede_estabilizar ?m - medico)
        ; Médico m aún puede estabilizar más víctimas (< 4)
        
        (puede_trasladar ?r - rescatista)
        ; Rescatista r aún puede hacerse cargo de más víctimas (< 5)
        
        ;; --- RECURSOS NECESARIOS PARA CONSTRUCCIÓN ---
        (requiere_tecnicos ?i - infraestructura)
        ; Infraestructura i requiere técnicos para construcción
        
        (requiere_obreros ?i - infraestructura)
        ; Infraestructura i requiere obreros
        
        (requiere_ingeniero ?i - infraestructura)
        ; Infraestructura i requiere ingeniero
        
        (requiere_operador ?i - infraestructura)
        ; Infraestructura i requiere operador permanente
        
        (requiere_maquinaria ?i - infraestructura)
        ; Infraestructura i requiere maquinaria pesada
        
        ;; --- CONTROL DE PERSONAL DE CONSTRUCCIÓN ---
        (personal_regresado ?p - personal_construccion)
        ; Personal de construcción p ha regresado a C0
        
        (operador_en_posicion ?op - operador ?l - locacion)
        ; Operador op está en posición en l
    )
    
    ;; =========================================================================
    ;; ACCIONES (Operaciones que modifican el estado del mundo)
    ;; =========================================================================
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: TRASLADAR UNIDAD MÓVIL
    ;; Mueve una unidad de una locación a otra adyacente
    ;; -------------------------------------------------------------------------
    (:action trasladar_unidad
        :parameters (?u - unidad_movil ?desde ?hacia - locacion)
        :precondition (and
            (en ?u ?desde)
            (adyacente ?desde ?hacia)
            (puede_avanzar_a ?hacia)
        )
        :effect (and
            (not (en ?u ?desde))
            (en ?u ?hacia)
            ; Las personas dentro se mueven con la unidad (implícito)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: CARGAR PERSONA EN UNIDAD
    ;; Sube una persona a una unidad móvil
    ;; -------------------------------------------------------------------------
    (:action cargar_persona
        :parameters (?p - persona ?u - unidad_movil ?l - locacion)
        :precondition (and
            (en ?p ?l)
            (en ?u ?l)
            (disponible ?p)
            (espacio_disponible ?u)
        )
        :effect (and
            (dentro ?p ?u)
            (not (disponible ?p))
            (not (en ?p ?l))
            ; Persona ahora se mueve con la unidad
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: DESCARGAR PERSONA DE UNIDAD
    ;; Baja una persona de una unidad móvil
    ;; -------------------------------------------------------------------------
    (:action descargar_persona
        :parameters (?p - persona ?u - unidad_movil ?l - locacion)
        :precondition (and
            (dentro ?p ?u)
            (en ?u ?l)
        )
        :effect (and
            (not (dentro ?p ?u))
            (disponible ?p)
            (en ?p ?l)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: CARGAR RECURSO EN UNIDAD
    ;; Carga un recurso pesado en unidad con capacidad de carga
    ;; -------------------------------------------------------------------------
    (:action cargar_recurso
        :parameters (?r - recurso ?u - unidad_movil ?l - locacion)
        :precondition (and
            (en ?r ?l)
            (en ?u ?l)
            (puede_transportar_carga ?u)
        )
        :effect (and
            (carga ?r ?u)
            (not (en ?r ?l))
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: DESCARGAR RECURSO DE UNIDAD
    ;; Descarga un recurso pesado de una unidad
    ;; -------------------------------------------------------------------------
    (:action descargar_recurso
        :parameters (?r - recurso ?u - unidad_movil ?l - locacion)
        :precondition (and
            (carga ?r ?u)
            (en ?u ?l)
        )
        :effect (and
            (not (carga ?r ?u))
            (en ?r ?l)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: CONSTRUIR PUENTE (PPF en C1)
    ;; Construye puente prefabricado con 3 técnicos
    ;; -------------------------------------------------------------------------
    (:action construir_puente_ppf
        :parameters (?p - puente ?l - locacion ?l_siguiente - locacion
                     ?t1 ?t2 ?t3 - tecnico)
        :precondition (and
            (en ?p ?l)
            (en ?t1 ?l)
            (en ?t2 ?l)
            (en ?t3 ?l)
            (disponible ?t1)
            (disponible ?t2)
            (disponible ?t3)
            (not (construido ?p))
            (adyacente ?l ?l_siguiente)
        )
        :effect (and
            (construido ?p)
            (operativo ?p)
            (conecta ?p ?l ?l_siguiente)
            (puede_avanzar_a ?l_siguiente)
            (tarea_completada ?p)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: CONSTRUIR CARRETERA (en C2)
    ;; Construye carretera con 10 obreros, ingeniero y 4 maquinarias
    ;; -------------------------------------------------------------------------
    (:action construir_carretera
        :parameters (?c - carretera ?l - locacion ?l_siguiente - locacion
                     ?i - ingeniero
                     ?o1 ?o2 ?o3 ?o4 ?o5 ?o6 ?o7 ?o8 ?o9 ?o10 - obrero
                     ?m1 ?m2 ?m3 ?m4 - maquinaria)
        :precondition (and
            (en ?i ?l)
            (en ?o1 ?l) (en ?o2 ?l) (en ?o3 ?l) (en ?o4 ?l) (en ?o5 ?l)
            (en ?o6 ?l) (en ?o7 ?l) (en ?o8 ?l) (en ?o9 ?l) (en ?o10 ?l)
            (en ?m1 ?l) (en ?m2 ?l) (en ?m3 ?l) (en ?m4 ?l)
            (disponible ?i)
            (disponible ?o1) (disponible ?o2) (disponible ?o3) (disponible ?o4) (disponible ?o5)
            (disponible ?o6) (disponible ?o7) (disponible ?o8) (disponible ?o9) (disponible ?o10)
            (not (construido ?c))
            (adyacente ?l ?l_siguiente)
        )
        :effect (and
            (construido ?c)
            (operativo ?c)
            (conecta ?c ?l ?l_siguiente)
            (puede_avanzar_a ?l_siguiente)
            (tarea_completada ?c)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: INSTALAR PUENTE COLGANTE (PCP en C3)
    ;; Instala puente colgante con 3 técnicos y operador
    ;; -------------------------------------------------------------------------
    (:action instalar_puente_colgante
        :parameters (?p - puente ?l - locacion ?l_siguiente - locacion
                     ?t1 ?t2 ?t3 - tecnico
                     ?op - operador)
        :precondition (and
            (en ?p ?l)
            (en ?t1 ?l)
            (en ?t2 ?l)
            (en ?t3 ?l)
            (en ?op ?l)
            (disponible ?t1)
            (disponible ?t2)
            (disponible ?t3)
            (disponible ?op)
            (not (construido ?p))
            (adyacente ?l ?l_siguiente)
        )
        :effect (and
            (construido ?p)
            (operativo ?p)
            (conecta ?p ?l ?l_siguiente)
            (puede_avanzar_a ?l_siguiente)
            (asignado_a_tarea ?op ?l)
            (operador_en_posicion ?op ?l)
            ; Nota: técnicos pueden regresar, operador NO
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: ESTABILIZAR VÍCTIMA GRAVE
    ;; Médico estabiliza una víctima grave
    ;; -------------------------------------------------------------------------
    (:action estabilizar_victima_grave
        :parameters (?m - medico ?v - victima_grave ?l - locacion)
        :precondition (and
            (en ?m ?l)
            (en ?v ?l)
            (disponible ?m)
            (disponible ?v)
            (puede_estabilizar ?m)
            (not (estabilizado ?v))
        )
        :effect (and
            (estabilizado ?v)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: REGISTRAR RESCATE
    ;; Marca una víctima como rescatada al llegar a la base
    ;; -------------------------------------------------------------------------
    (:action registrar_rescate
        :parameters (?v - victima ?l - locacion)
        :precondition (and
            (en ?v ?l)
            (base ?l)
            (disponible ?v)
            ; Si es víctima grave, debe estar estabilizada
            (or
                (not (requiere_estabilizacion ?v))
                (estabilizado ?v)
            )
        )
        :effect (and
            (rescatado ?v)
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: RETORNAR PERSONAL DE CONSTRUCCIÓN
    ;; Personal regresa a base después de completar tarea
    ;; -------------------------------------------------------------------------
    (:action retornar_personal_construccion
        :parameters (?p - personal_construccion ?u - unidad_movil 
                     ?l_actual - locacion ?l_base - locacion)
        :precondition (and
            (en ?p ?l_actual)
            (en ?u ?l_actual)
            (disponible ?p)
            (base ?l_base)
            (espacio_disponible ?u)
            ; Puede regresar solo después de completar tarea
        )
        :effect (and
            (dentro ?p ?u)
            (not (disponible ?p))
            (not (en ?p ?l_actual))
        )
    )
    
    ;; -------------------------------------------------------------------------
    ;; ACCIÓN: RETORNAR OPERADOR (Última acción del rescate)
    ;; Operador regresa después de que todos crucen
    ;; -------------------------------------------------------------------------
    (:action retornar_operador
        :parameters (?op - operador ?u - unidad_movil 
                     ?l_actual - locacion ?l_base - locacion)
        :precondition (and
            (operador_en_posicion ?op ?l_actual)
            (en ?u ?l_actual)
            (base ?l_base)
            (espacio_disponible ?u)
            ; Esta acción debe ejecutarse después del rescate
            ; (implícito en el orden del plan)
        )
        :effect (and
            (dentro ?op ?u)
            (not (operador_en_posicion ?op ?l_actual))
            (not (asignado_a_tarea ?op ?l_actual))
            (disponible ?op)  ; Marca que ya no está asignado
        )
    )
)

