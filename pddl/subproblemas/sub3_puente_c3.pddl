;; =============================================================================
;; SUB-PROBLEMA 3: INSTALAR PUENTE COLGANTE EN C3
;; Precondición: PPF y Carretera ya construidos
;; Objetivo: Instalar PCP, operador se queda, técnicos regresan
;; =============================================================================

(define (problem sub3-puente-c3)
    (:domain rescate-mina)
    
    (:objects
        C0 C1 C2 C3 M - locacion
        UX U3 - unidad_movil
        TecnicoC3_1 TecnicoC3_2 TecnicoC3_3 - tecnico
        Operador1 - operador
        PCP - puente
        PPF - puente
        Carretera_C2 - carretera
    )
    
    (:init
        ;; Clasificación
        (base C0)
        (zona_estacionamiento C1)
        (zona_estacionamiento C2)
        (zona_estacionamiento C3)
        
        ;; Topología
        (adyacente C0 C1)
        (adyacente C1 C0)
        (adyacente C1 C2)
        (adyacente C2 C1)
        (adyacente C2 C3)
        (adyacente C3 C2)
        (adyacente C3 M)
        (adyacente M C3)
        
        ;; Permisos (PPF y Carretera operativos)
        (puede_avanzar_a C0)
        (puede_avanzar_a C1)
        (puede_avanzar_a C2)
        (puede_avanzar_a C3)
        
        ;; Infraestructura previa construida
        (construido PPF)
        (operativo PPF)
        (conecta PPF C1 C2)
        
        (construido Carretera_C2)
        (operativo Carretera_C2)
        (conecta Carretera_C2 C2 C3)
        
        ;; Unidades en C0
        (en UX C0)
        (puede_transportar_carga UX)
        (espacio_disponible UX)
        
        (en U3 C0)
        (espacio_disponible U3)
        
        ;; Personal en C0
        (en TecnicoC3_1 C0)
        (en TecnicoC3_2 C0)
        (en TecnicoC3_3 C0)
        (en Operador1 C0)
        
        (disponible TecnicoC3_1)
        (disponible TecnicoC3_2)
        (disponible TecnicoC3_3)
        (disponible Operador1)
        
        ;; Puente colgante en C0
        (en PCP C0)
        (not (construido PCP))
        (not (operativo PCP))
    )
    
    (:goal (and
        ;; Puente colgante operativo
        (construido PCP)
        (operativo PCP)
        (puede_avanzar_a M)
        
        ;; Operador asignado en C3 (SE QUEDA)
        (asignado_a_tarea Operador1 C3)
        (operador_en_posicion Operador1 C3)
        
        ;; Técnicos de regreso en C0
        (en TecnicoC3_1 C0)
        (en TecnicoC3_2 C0)
        (en TecnicoC3_3 C0)
        
        ;; Unidades de regreso
        (en UX C0)
        (en U3 C0)
    ))
)

