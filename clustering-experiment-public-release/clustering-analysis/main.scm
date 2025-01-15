(use-modules (json)
             (srfi srfi-9)
             (srfi srfi-1)
             (srfi srfi-26)
             (srfi srfi-42)
             (sxml simple)
             (ice-9 ftw)
             (ice-9 threads))

(eval-when (compile load eval)
  (define identifier->string (compose symbol->string syntax->datum))
  (define (string->identifier syntax str)
    (datum->syntax syntax (string->symbol str))))

(define-syntax transform-identifier
  (syntax-rules ()
    ((transform-identifier ident body body* ...)
     (string->identifier ident
                         (let ((ident (identifier->string ident)))
                           body body* ...)))))

(define-syntax quick-record
  (lambda (stx)

    (define (postfix prefix . strs)
      (transform-identifier prefix
                            (apply string-append prefix strs)))

    (define (pprefix postfix str)
      (transform-identifier postfix
                            (string-append str postfix)))

    (define (surround-brackets item)
      (string->identifier item (string-append "<"
                                         (identifier->string item)
                                         ">")))

    (define (generate-get-set prefix field)
      (with-syntax ([set (postfix prefix "-" (identifier->string field) "-set!")]
                    [get (postfix prefix "-" (identifier->string field))]
                    [field field])
                   #'(field get set)))

    (define (generate-get-sets prefix fields)
      (map
        (lambda (field) (generate-get-set prefix field))
        fields))

    (syntax-case stx ()
                 ((_ prefix field field* ...)
                  (let ((get-sets (generate-get-sets #'prefix #'(field field* ...))))
                        (with-syntax ([record-name (surround-brackets #'prefix)]
                                      [predicate (postfix #'prefix "?")]
                                      [constructor-name (pprefix #'prefix "make-")])
                                     #`(define-record-type record-name
                                         (constructor-name field field* ...)
                                         predicate
                                         #,@get-sets)))))))


(quick-record clustering
              points
              number-of-points
              group
              boundary
              clusters
              base-uuid
              unique-uuid)

(quick-record cluster
              points
              start-time
              end-time
              edge-points)


(define (json-trial->clustering trial)
  (let* ((base-uuid (assoc-ref trial "base_uuid"))
         (unique-uuid (assoc-ref trial "unique_uuid"))
         (number-of-points (assoc-ref trial "number_of_points"))
         (group (assoc-ref trial "group"))
         (json-clusters (assoc-ref trial "clusters"))
         (convert-json-cluster-points (lambda (json-cluster)
                                        (list-ec (: json-point (assoc-ref json-cluster "points"))
                                                 (cons (assoc-ref json-point "x")
                                                       (assoc-ref json-point "y")))))
         (clusters (list-ec (: json-cluster json-clusters)
                            (convert-json-cluster-points json-cluster)))
         (points (concatenate clusters))
         (start-time (assoc-ref trial "startTimestamp"))
         (end-time (assoc-ref trial "endTimestamp")))
    (make-clustering points number-of-points
                     group
                     #f
                     (list-ec (: json-cluster json-clusters)
                              (make-cluster (convert-json-cluster-points json-cluster)
                                            #f
                                            #f
                                            (list-ec (: json-point (assoc-ref json-cluster "edgePoints"))
                                                     (cons (assoc-ref json-point "x")
                                                           (assoc-ref json-point "y")))))
                     base-uuid
                     unique-uuid)))

(define (clusterings-from-file path)
  (map json-trial->clustering (vector->list (call-with-input-file path json->scm))))

(define (sum numbers)
  (fold + 0 numbers))

(define (mean numbers)
  (/ (sum numbers) (length numbers)))

(define (centroid-of-points points)
  (let ((xs (map car points))
        (ys (map cdr points)))
    (cons (exact->inexact (mean xs))
          (exact->inexact (mean ys)))))

(define (cluster-centroid cluster)
  (centroid-of-points (cluster-points cluster)))

(define (make-list-cycler lst)
  (let ((current lst))
    (lambda ()
      (if (null? current)
          (begin (set! current (cdr lst))
                 (car lst))
          (let ((ret (car current)))
            (set! current (cdr current))
            ret)))))

(define svg-colors '("crimson" "blue" "darkcyan" "fuchsia" "grey" "plum" "salmon" "midnightblue" "brown" "orange" "purple"))

(define (sxml->xml-string sxml)
  (call-with-output-string
    (lambda (port) (sxml->xml sxml port))))

(define (visualize-clustering clustering)
  (let ((cluster-elements
         (concatenate (let ((color-cycler (make-list-cycler svg-colors)))
                        (do ((i 0 (+ i 1))
                             (clusters (clustering-clusters clustering) (cdr clusters))
                             (ret '() (cons (let* ((cluster (car clusters))
                                                   (color (color-cycler))
                                                   (centroid (cluster-centroid cluster))
                                                   (edge-path-d (let* ((first-point (car (cluster-edge-points cluster)))
                                                                       (rest-of-points (cdr (cluster-edge-points cluster))))
                                                                  (string-join (cons
                                                                                (string-append "M " (number->string (car first-point))
                                                                                               " "
                                                                                               (number->string (cdr first-point)))
                                                                                (append (map (lambda (point)
                                                                                               (string-append "L " (number->string (car point))
                                                                                                              " " (number->string (cdr point))))
                                                                                             rest-of-points)
                                                                                        (list "Z")))
                                                                               " "))))
                                              (append
                                               (list
                                                `(text (@ (x ,(number->string (car centroid)))
                                                         (y ,(number->string (cdr centroid)))
                                                         (text-anchor "middle")
                                                         (fill "black")
                                                         (font-size "2em"))
                                                       ,(number->string i))
                                                `(path (@ (d ,edge-path-d)
                                                          (stroke "black")
                                                          (fill "none"))))
                                               (list-ec (: point (clustering-points cluster))
                                                        (let ((x (number->string (car point)))
                                                              (y (number->string (cdr point))))
                                                          `(circle (@ (cx ,x) (cy ,y) (r "5") (fill ,color)))))))
                                            ret)))
                            ((null? clusters) ret))))))

    `(*TOP* (svg (@ (height 500) (width 800))
                 (rect (@ (width 800)
                          (height 500)
                          (fill "white")))
                 ,@cluster-elements))))


(define (visualize-clustering-stimulus points)
  (let* ((cluster-elements (list-ec (: point points)
                                    (let ((x (number->string (car point)))
                                          (y (number->string (cdr point))))
                                      `(circle (@ (cx ,x) (cy ,y) (r "5") (fill "black")))))))
    `(*TOP* (svg (@ (height 500) (width 800))
                 (rect (@ (width 800)
                          (height 500)
                          (fill "white")
                          (style "stroke-width: 2; stroke: black;")))
                 ,@cluster-elements))))

(system* "mkdir" "-p" "build/cluster-images")

;; (let* ((base-path "data/normalized_clustering_trials")
;;        (json-files (map
;;                     (cut string-append base-path "/" <>)
;;                     (filter
;;                      (cut string-suffix? ".json" <>)
;;                      (cddr (scandir base-path))))))
;;   (par-for-each
;;    (lambda (json-path)
;;      (let* ((clusterings (clusterings-from-file json-path)))
;;        (do ((i 0 (+ i 1))
;;             (clusterings clusterings (cdr clusterings)))
;;            ((null? clusterings))
;;          (let* ((sxml (visualize-clustering (car clusterings)))
;;                 (output-path (string-append "build/cluster-images/" (basename json-path ".json")
;;                                             "-" (number->string i)  ".svg")))
;;            (call-with-output-file output-path
;;              (lambda (port)
;;                (display (sxml->xml-string sxml) port)))))))
;;    json-files))

(system* "mkdir" "-p" "build/stimulus-images")

(define build-pdfs?
  (let ((args (command-line)))
    (cond
     ((< (length args) 2)
      (error "Provide an argument (true/false), true to convert the svgs to pdfs and pngs or false to not."))
     ((not (member (list-ref args 1) '("true" "false")))
      (error "Provide a well formatted argument, true to convert the svgs to pdfs and pngs or false to not."))
     ((string=? (list-ref args 1) "true")
      #t)
     (else #f))))

(define status-mutex (make-mutex))

(let* ((base "stimuli/experiment-1-2-3/stimuli_json/")
       (stim-files (map
                    (lambda (name) (string-append base name))
                    (scandir base
                             (lambda (path) (string-suffix? ".json" path)))))
       (json-data (map (lambda (path) (call-with-input-file path json->scm)) stim-files))
       (filter (lambda (stim) (and (not (assoc-ref stim "practice_stimulus"))
                                   (not (assoc-ref stim "flipped"))))))
  (let ((n-stim (length json-data)))
    (for-each
     (lambda (stim i)
       (let* ((points (map (lambda (point) (cons (assoc-ref point "x")
                                                 (assoc-ref point "y")))
                           (vector->list (assoc-ref stim "points"))))
              (svg-contents (visualize-clustering-stimulus points))
              (outpath (string-append "build/stimulus-images/" (assoc-ref stim "base_uuid") ".svg"))
              (pngoutpath (string-append "build/stimulus-images/" (assoc-ref stim "base_uuid") ".png"))
              (pdfoutpath (string-append "build/stimulus-images/" (assoc-ref stim "base_uuid") ".pdf")))
         (call-with-output-file outpath
           (lambda (port)
             (display (sxml->xml-string svg-contents) port)
             (newline port)))
         (when build-pdfs?
           (with-mutex status-mutex
             (format #t "~a% done!\n" (round (* 100 (exact->inexact (/ i (- n-stim 1)))))))
           (system* "inkscape" "-D" outpath "-o" pdfoutpath "--export-latex")
           (system* "inkscape" "-D" outpath "-o" pngoutpath))))
     json-data (iota n-stim)))
  
  ;; (let-syntax ((add-item (syntax-rules ()
  ;;                          ((_ var item)
  ;;                           (set! var (cons (cons (assoc-ref item "base_uuid")
  ;;                                                 (assoc-ref item "number_of_points")) var))))))
  ;;   (let ((c '())
  ;;         (d '())
  ;;         (retrieve-with-n-points (lambda (n l)
  ;;                                   (find (lambda (item)
  ;;                                           (= (cdr item) n))
  ;;                                        l))))
  ;;     (for-each
  ;;      (lambda (stim)
  ;;        (cond
  ;;         ((eq? (assoc-ref stim "group") 'null) #f)
  ;;         ((string=? (assoc-ref stim "group") "clustered") (add-item c stim))
  ;;         ((string=? (assoc-ref stim "group") "disperse") (add-item d stim))))
  ;;      json-data)
  ;;     (for-each
  ;;      (lambda (n)
  ;;        (format #t "Clustered: ~a, Dispersed: ~a~%" (retrieve-with-n-points n c)
  ;;            (retrieve-with-n-points n d)))
  ;;      '(10 15 20 25 30 35 40))))
  )

(display "Example clusterings figure base_uuids\n")

      (display "(\"b3697dbc-04ee-4762-a98d-5773cf0c7e84\" . 10) (\"3088609a-8abd-42eb-9289-926728077ed5\" . 10)
(\"3c4d6c38-877b-41d2-b2b5-d2f74ef0970b\" . 15) (\"d26cc3de-4659-421d-a01c-1b05a01a5457\" . 15)
(\"339f68e4-98bf-4d4a-81c7-06fa958f307e\" . 20) (\"49f28baf-c341-4fb1-a75b-0ff70240de39\" . 20)
(\"2bb1495b-1ef6-4943-bb48-662371f50b30\" . 25) (\"87cc45a4-3e2e-4c67-a9d6-3ba04eda2588\" . 25)
(\"51196345-76b0-41da-9c00-5ecb1a87b408\" . 30) (\"a817f837-f86b-4b90-88a3-572342420271\" . 30)
(\"98dd5bec-729c-46ed-9714-b1e26e817196\" . 35) (\"0f9a9c80-cdab-4071-8d56-27965b585a10\" . 35)
(\"fdb55140-d76a-43e5-b66a-8883dc677b94\" . 40) (\"d764a7da-3857-4975-a325-f83a0b413cc5\" . 40)
")




       ;; (let ((caption (format #f "Stimulus: ~a, Number of Points: ~a, Cluster Structure: ~a"
       ;;                               (assoc-ref stim "base_uuid")
       ;;                               (assoc-ref stim "number_of_points")
       ;;                               (cond
       ;;                                ((eq? (assoc-ref stim "group") 'null) "None")
       ;;                                ((string=? (assoc-ref stim "group") "clustered") "Clustered")
       ;;                                ((string=? (assoc-ref stim "group") "disperse") "Dispersed")))))
       ;;          (format #t "\\begin{center}
       ;; \\captionof{figure}{~a}
       ;; \\includegraphics[width=0.66\\textwidth]{~a}
       ;; \\end{center}\\clearpage{}~%~%"
       ;;                  caption
       ;;                  (string-append "images/stimulus-images/" (assoc-ref stim "base_uuid") ".pdf")))
