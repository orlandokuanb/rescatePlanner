;; =============================================================================
;; SUB-PROBLEMA 1: CONSTRUIR PUENTE EN C1
;; Objetivo: Transportar PPF y técnicos, construir puente, retornar personal
;; =============================================================================

(define (problem sub1-puente-c1)
    (:domain rescate-mina)
    
    (:objects
        C0 C1 C2 - locacion
        U1 - unidad_movil
        TecnicoC1_1 TecnicoC1_2 TecnicoC1_3 - tecnico
        PPF - puente
    )
    
    (:init
        ;; Clasificación
        (base C0)
        (zona_estacionamiento C1)
        
        ;; Topología
        (adyacente C0 C1)
        (adyacente C1 C0)
        (adyacente C1 C2)
        (adyacente C2 C1)
        
        ;; Permisos
        (puede_avanzar_a C0)
        (puede_avanzar_a C1)
        
        ;; Unidad en C0
        (en U1 C0)
        (espacio_disponible U1)
        (puede_transportar_carga U1)
        
        ;; Personal en C0
        (en TecnicoC1_1 C0)
        (en TecnicoC1_2 C0)
        (en TecnicoC1_3 C0)
        (disponible TecnicoC1_1)
        (disponible TecnicoC1_2)
        (disponible TecnicoC1_3)
        
        ;; Puente en C0
        (en PPF C0)
        (not (construido PPF))
        (not (operativo PPF))
    )
    
    (:goal (and
        ;; Puente construido y operativo
        (construido PPF)
        (operativo PPF)
        (puede_avanzar_a C2)
        
        ;; Personal de regreso en C0
        (en TecnicoC1_1 C0)
        (en TecnicoC1_2 C0)
        (en TecnicoC1_3 C0)
        
        ;; Unidad de regreso en C0
        (en U1 C0)
    ))
)

