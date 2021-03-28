 <code>
    pip install requirements.txt
    <br>
    python manage.py runsever


 </code>

<hr>
<pre>
                <p>Task 1</p>
            <code >
               API for getting ticket  <span class="badge badge-primary">ACCEPTS GET REQUEST</span>
               <kbd >/api/get-ticket/</kbd>
            </code>
            </pre>

<hr>

<pre>
                <p>Task 2</p>
                <code class="">
                   API for getting lucky draws
                    <span class="badge badge-primary">ACCEPTS GET REQUEST</span>
                   <kbd >/api/get-lucky-draws/</kbd>
                </code>
                </pre>

<hr>
<pre>
                <p>Task 3</p>
                <code class="">
                   API for participating in lucky draw
                     <span class="badge badge-primary">ACCEPTS POST REQUEST</span>
                   <kbd >/api/participate-in-game/</kbd>
                    <code>
                    {
                    "ticket_id" : "{TICKET ID}" , 
                    "lucky_draw_id" : "{LUCKY DRAW ID}" 
                    }
             </code>
                </code>
                </pre>


<hr>

<pre>
                <p>Task 4</p>
                <code >API for listing winners  <span class="badge badge-danger">ACCEPTS GET REQUEST</span>
                <kbd >/api/get-winners/</kbd>
                
             </pre>

<hr>
<pre>
                <p>Task 5</p>
             <code >API for computing winners. <span class="badge badge-success">ACCEPTS POST REQUEST</span>
                <kbd >/update/</kbd>
                <code>
                    {
                    "lucky_draw_id" : "{LUCKY DRAW ID}" , 
                    "current_date" : "{DATE OF LUCKY DRAW}" 
                    }
            
            </code>
            


<hr>




</div>