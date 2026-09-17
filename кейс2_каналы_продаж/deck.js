const PptxGenJS = require('pptxgenjs');
const p = new PptxGenJS();
p.layout = 'LAYOUT_WIDE';                       // 13.33 x 7.5
p.author = 'Кейс 2'; p.title = 'Анализ каналов продаж';

const NAVY='14213D', AMBER='FCA311', W='FFFFFF', GREY='6B7280', LIGHT='F1F2F4',
      DIM='C9CDD6', RED='C1121F', INK='1F2937';
const H='Cambria', B='Calibri';
const CH=['сайт','директ','LaModa','Блогеры','ВК'];

const t = (s,txt,o)=>s.addText(txt,Object.assign({isTextBox:true,margin:0},o));
const card=(s,x,y,w,h,fill)=>s.addShape(p.ShapeType.roundRect,{x,y,w,h,rectRadius:0.06,
  fill:{color:fill||LIGHT},line:{type:'none'}});
const circle=(s,x,y,d,fill)=>s.addShape(p.ShapeType.ellipse,{x,y,w:d,h:d,
  fill:{color:fill||AMBER},line:{type:'none'}});
const head=(s,title,sub)=>{
  t(s,title,{x:0.6,y:0.42,w:12.1,h:0.72,fontFace:H,fontSize:34,bold:true,color:NAVY});
  if(sub) t(s,sub,{x:0.6,y:1.16,w:12.1,h:0.42,fontFace:B,fontSize:14,color:GREY});
};
const stat=(s,x,y,w,val,lab,note,vc,bg)=>{
  const dark = bg===NAVY;                       // на тёмной карточке подписи светлые
  card(s,x,y,w,note?1.95:1.6,bg||LIGHT);
  t(s,val,{x:x+0.28,y:y+0.2,w:w-0.56,h:0.72,fontFace:B,fontSize:32,bold:true,color:vc||NAVY});
  t(s,lab,{x:x+0.28,y:y+0.94,w:w-0.56,h:0.32,fontFace:B,fontSize:13,bold:true,color:dark?W:INK});
  if(note) t(s,note,{x:x+0.28,y:y+1.28,w:w-0.56,h:0.55,fontFace:B,fontSize:11,color:dark?DIM:GREY});
};
const band=(s,y,txt,h)=>{
  s.addShape(p.ShapeType.roundRect,{x:0.6,y,w:12.1,h:h||1.25,rectRadius:0.05,
    fill:{color:NAVY},line:{type:'none'}});
  t(s,txt,{x:1.0,y:y+0.2,w:11.3,h:(h||1.25)-0.4,fontFace:B,fontSize:15,color:W,valign:'middle'});
};
const chartBase={showLegend:false,showTitle:false,showValue:true,dataLabelFontFace:B,
  dataLabelFontSize:12,dataLabelColor:INK,catAxisLabelFontFace:B,catAxisLabelFontSize:12,
  catAxisLabelColor:INK,valAxisLabelFontFace:B,valAxisLabelFontSize:11,valAxisLabelColor:GREY,
  catGridLine:{style:'none'},valGridLine:{color:'E5E7EB',size:1},barGapWidthPct:55};

/* 1 — титул */
let s=p.addSlide(); s.background={color:NAVY};
s.addShape(p.ShapeType.ellipse,{x:10.1,y:-1.4,w:5.4,h:5.4,fill:{color:AMBER,transparency:88},line:{type:'none'}});
t(s,'АНАЛИЗ КАНАЛОВ ПРОДАЖ',{x:0.8,y:1.55,w:9.6,h:1.7,fontFace:H,fontSize:44,bold:true,color:W,lineSpacing:46});
t(s,'Спортивные футболки с принтом · пять каналов · срез за месяц',
  {x:0.8,y:3.35,w:9.6,h:0.45,fontFace:B,fontSize:18,color:AMBER});
[['82','футболки продано'],['271 200 ₽','выручка за месяц'],['2,58','маржи на рубль рекламы']]
 .forEach(([v,l],i)=>{const x=0.8+i*3.5;
  t(s,v,{x,y:4.5,w:3.2,h:0.7,fontFace:B,fontSize:36,bold:true,color:W});
  t(s,l,{x,y:5.25,w:3.2,h:0.35,fontFace:B,fontSize:12,color:DIM});});
t(s,'Кейс 2 · ИТМО, Управление высокотехнологичным бизнесом',
  {x:0.8,y:6.55,w:9.6,h:0.35,fontFace:B,fontSize:11,color:GREY});
s.addNotes('Продаём спортивные футболки с принтом. За месяц 82 продажи, 271 200 ₽ выручки. Каждый рубль рекламы вернул 2,58 рубля маржи. Дальше — откуда эти деньги и куда их двигать.');

/* 2 — юнит-экономика */
s=p.addSlide(); head(s,'Экономика одной футболки','Цифры взяты из бюджета проекта — Кейс 1');
stat(s,0.6,1.85,3.9,'3 390 ₽','Цена в рознице','Средний чек. У блогеров 3 051 ₽ — промокод −10%');
stat(s,4.72,1.85,3.9,'851 ₽','Себестоимость юнита','Футболка 780 + принт 46 + упаковка 25');
stat(s,8.84,1.85,3.86,'2 171 ₽','Маржа с заказа','На своём сайте — после эквайринга и доставки',AMBER,NAVY);
band(s,4.25,'На LaModa маржа падает до 1 202 ₽ — площадка забирает 35% комиссии.\nОдин и тот же товар приносит вдвое разные деньги в зависимости от канала.',1.4);
t(s,'Именно поэтому сравнивать каналы по выручке бессмысленно — сравниваем по марже.',
  {x:0.6,y:6.0,w:12.1,h:0.4,fontFace:B,fontSize:13,italic:true,color:GREY});
s.addNotes('Ключ ко всему разбору: маржа зависит от канала. Своя площадка — 2 171 ₽, маркетплейс — 1 202 ₽.');

/* 3 — методика */
s=p.addSlide(); head(s,'Как считаем','Одна воронка из четырёх шагов — одинаково для всех пяти каналов');
[['1','Показы','386 000'],['2','Переходы','5 560'],['3','Корзина','508'],['4','Продажи','82']]
 .forEach(([n,l,v],i)=>{const x=0.6+i*3.15;
  card(s,x,1.95,2.8,1.85);
  circle(s,x+0.25,2.18,0.42);
  t(s,n,{x:x+0.25,y:2.24,w:0.42,h:0.3,fontFace:B,fontSize:14,bold:true,color:NAVY,align:'center'});
  t(s,l,{x:x+0.8,y:2.22,w:1.8,h:0.34,fontFace:B,fontSize:14,bold:true,color:INK});
  t(s,v,{x:x+0.25,y:2.85,w:2.3,h:0.7,fontFace:B,fontSize:26,bold:true,color:NAVY});
  if(i<3) t(s,'→',{x:x+2.82,y:2.6,w:0.33,h:0.4,fontFace:B,fontSize:18,bold:true,color:AMBER,align:'center'});});
t(s,'Четыре метрики решения',{x:0.6,y:4.35,w:12.1,h:0.4,fontFace:B,fontSize:16,bold:true,color:NAVY});
[['Цена перехода','затрачено / переходы'],['Цена клиента (CAC)','затрачено / продажи'],
 ['ROAS','прибыль / затрачено'],['ДРР','затрачено / выручка']]
 .forEach(([a,b2],i)=>{const x=0.6+i*3.15;
  t(s,a,{x,y:4.85,w:2.9,h:0.32,fontFace:B,fontSize:14,bold:true,color:INK});
  t(s,b2,{x,y:5.2,w:2.9,h:0.32,fontFace:B,fontSize:12,color:GREY});});
band(s,5.8,'ROAS считаем по марже, а не по выручке: он показывает, сколько живых денег возвращает рубль рекламы.',0.95);
s.addNotes('Воронка одна для всех каналов, поэтому их можно честно сравнивать. ROAS по марже, не по выручке.');

/* 4 — результат */
s=p.addSlide(); head(s,'Результат месяца');
[['82','продажи','',NAVY,LIGHT],['271 200 ₽','выручка','',NAVY,LIGHT],
 ['85 457 ₽','денег в кассе','',NAVY,LIGHT],['2,58','ROAS по компании','',AMBER,NAVY]]
 .forEach(([v,l,n,c,bg],i)=>stat(s,0.6+i*3.09,1.8,2.84,v,l,null,c,bg));
band(s,3.7,'Все пять каналов окупают рекламу — убыточных нет.\nВопрос не «кого выключить», а «куда переложить»: разброс эффективности десятикратный.',1.45);
[['Лучший','сайт — 5,64 на рубль'],['Худший','ВК — 1,23 на рубль'],['Бюджет месяца','54 000 ₽ на пять каналов']]
 .forEach(([a,b2],i)=>{const x=0.6+i*4.05;
  t(s,a,{x,y:5.5,w:3.8,h:0.3,fontFace:B,fontSize:12,color:GREY});
  t(s,b2,{x,y:5.83,w:3.8,h:0.36,fontFace:B,fontSize:16,bold:true,color:INK});});
s.addNotes('Бизнес в плюсе, все каналы окупаются. Но разброс между лучшим и худшим — в 4,6 раза.');

/* 5 — таблица */
s=p.addSlide(); head(s,'Каналы в цифрах','Затраты, отдача и цена клиента по каждому каналу');
const hd=t2=>({text:t2,options:{bold:true,color:W,fill:{color:NAVY},fontSize:13,align:'center'}});
const rowsT=[
 ['Продажи, шт','13','12','30','20','7','82'],
 ['Затрачено, ₽','5 000','12 000','12 000','15 000','10 000','54 000'],
 ['Прибыль с продаж, ₽','28 223','26 052','36 060','36 780','12 342','139 457'],
 ['Деньги в кассе, ₽','23 223','14 052','24 060','21 780','2 342','85 457'],
 ['Цена клиента, ₽','385','1 000','400','750','1 429','659'],
 ['ROAS','5,64','2,17','3,01','2,45','1,23','2,58']];
s.addTable([[hd('Метрика'),...CH.map(hd),hd('ИТОГО')],
  ...rowsT.map((r,ri)=>r.map((c,ci)=>({text:c,options:{
    fontSize:13,bold:ri===5||ci===0,align:ci?'center':'left',
    color:ri===5&&ci>0?(parseFloat(c.replace(',','.'))>=2.58?NAVY:RED):INK,
    fill:{color:ri%2?W:LIGHT}}})))],
  {x:0.6,y:1.75,w:12.1,colW:[2.8,1.55,1.55,1.55,1.55,1.55,1.55],rowH:0.52,
   fontFace:B,border:{type:'solid',color:'E5E7EB',pt:1},valign:'middle'});
t(s,'Красным — каналы ниже среднего по компании. Цена клиента у ВК (1 429 ₽) съедает 81% его маржи.',
  {x:0.6,y:5.6,w:12.1,h:0.4,fontFace:B,fontSize:13,color:GREY});
s.addNotes('Таблица-основа. Обратите внимание: LaModa даёт больше всех продаж и денег, ВК — меньше всех при втором по размеру бюджете.');

/* 6 — ROAS */
s=p.addSlide(); head(s,'Возврат на рубль рекламы','ROAS = прибыль с продаж / затраты. Порог окупаемости — 1,0');
s.addChart(p.ChartType.bar,[{name:'ROAS',labels:['сайт','LaModa','Блогеры','директ','ВК'],
  values:[5.64,3.01,2.45,2.17,1.23]}],Object.assign({},chartBase,
  {x:0.5,y:1.75,w:7.8,h:4.4,barDir:'col',chartColors:[AMBER,NAVY,NAVY,NAVY,RED],
   dataLabelPosition:'outEnd',dataLabelFormatCode:'0.00',valAxisMaxVal:6}));
[['Сайт — 5,64','Органика почти бесплатна: платим 5 000 ₽ за SEO, а не за клики'],
 ['LaModa — 3,01','Чужой трафик, но и чужая комиссия 35%'],
 ['ВК — 1,23','Держится только на малом бюджете: ДРР 42%']]
 .forEach(([a,b2],i)=>{const y=2.1+i*1.45;
  circle(s,8.7,y,0.3,i===2?RED:AMBER);
  t(s,a,{x:9.15,y:y-0.03,w:3.6,h:0.35,fontFace:B,fontSize:15,bold:true,color:NAVY});
  t(s,b2,{x:9.15,y:y+0.35,w:3.55,h:0.85,fontFace:B,fontSize:12,color:GREY});});
s.addNotes('Разброс в 4,6 раза. Сайт выигрывает не объёмом, а тем, что мы не покупаем клики.');

/* 7 — эффективность vs деньги */
s=p.addSlide(); head(s,'Эффективность ≠ деньги','Один и тот же месяц, два разных рейтинга');
[['По эффективности (ROAS)',['сайт — 5,64','LaModa — 3,01','Блогеры — 2,45','директ — 2,17','ВК — 1,23'],0.6],
 ['По деньгам в кассе',['LaModa — 24 060 ₽','сайт — 23 223 ₽','Блогеры — 21 780 ₽','директ — 14 052 ₽','ВК — 2 342 ₽'],6.85]]
 .forEach(([title,list,x])=>{
  card(s,x,1.8,5.85,3.4);
  t(s,title,{x:x+0.4,y:2.0,w:5.05,h:0.4,fontFace:B,fontSize:16,bold:true,color:NAVY});
  list.forEach((li,i)=>{
    circle(s,x+0.4,2.55+i*0.55,0.3,i===0?AMBER:'D7DAE0');
    t(s,String(i+1),{x:x+0.4,y:2.59+i*0.55,w:0.3,h:0.26,fontFace:B,fontSize:12,bold:true,color:NAVY,align:'center'});
    t(s,li,{x:x+0.85,y:2.57+i*0.55,w:4.6,h:0.32,fontFace:B,fontSize:14,color:INK});});});
band(s,5.45,'Сайт — самый эффективный, но он упёрся в потолок: 260 переходов, SEO деньгами не разгонишь.\nLaModa — самый денежный: берёт объём сразу, платим за это комиссией.',1.4);
s.addNotes('Главная мысль защиты: у каналов разные роли. Эффективность и объём — не одно и то же.');

/* 8 — парадокс LaModa */
s=p.addSlide(); head(s,'Парадокс LaModa','Лучшая воронка в таблице — и худшая маржа');
s.addChart(p.ChartType.bar,[{name:'Маржа с заказа, ₽',labels:['сайт','директ','Блогеры','ВК','LaModa'],
  values:[2171,2171,1839,1763,1202]}],Object.assign({},chartBase,
  {x:0.5,y:1.8,w:7.3,h:4.3,barDir:'col',chartColors:[NAVY,NAVY,NAVY,NAVY,AMBER],
   dataLabelPosition:'outEnd',dataLabelFormatCode:'#,##0'}));
t(s,'Вход лучший из всех',{x:8.2,y:2.0,w:4.5,h:0.36,fontFace:B,fontSize:16,bold:true,color:NAVY});
t(s,'3,00% из показа в переход — втрое лучше сайта и директа. Человек уже внутри магазина одежды.',
  {x:8.2,y:2.4,w:4.5,h:0.9,fontFace:B,fontSize:13,color:GREY});
t(s,'Цена — комиссия 35%',{x:8.2,y:3.5,w:4.5,h:0.36,fontFace:B,fontSize:16,bold:true,color:NAVY});
t(s,'1 202 ₽ с заказа вместо 2 171 ₽. Мы платим не за трафик, а за чужое доверие: возврат, примерку, отзывы.',
  {x:8.2,y:3.9,w:4.5,h:1.1,fontFace:B,fontSize:13,color:GREY});
band(s,5.5,'Вывод: LaModa наращиваем ради объёма и оборота, но прибыль на единицу растёт только на своём сайте.',1.05);
s.addNotes('Если спросят, почему не залить всё в LaModa: потому что каждая футболка там приносит вдвое меньше.');

/* 9 — где теряем */
s=p.addSlide(); head(s,'Где теряется покупатель','Сквозная воронка по всем каналам');
[['1,44%','показ → переход','386 000 показов дали 5 560 переходов'],
 ['9,14%','переход → корзина','из 5 560 в корзину попали 508'],
 ['16,14%','корзина → оплата','из 508 корзин оплачены 82']]
 .forEach(([v,l,n],i)=>stat(s,0.6+i*4.12,1.8,3.86,v,l,n,i===2?RED:NAVY));
t(s,'Узкое место по каналам',{x:0.6,y:4.1,w:12.1,h:0.4,fontFace:B,fontSize:16,bold:true,color:NAVY});
[['сайт','вход: 1% из показов — мы в выдаче, но не в топе'],
 ['директ','корзина 8% и оплата 12,5% — самая холодная аудитория'],
 ['LaModa','узких мест нет, ограничение — комиссия'],
 ['Блогеры','оплата 12,5%: доверие блогеру ≠ доверие бренду'],
 ['ВК','вход 2,86% в корзину — в 7 раз хуже сайта']]
 .forEach(([a,b2],i)=>{const y=4.6+i*0.42;
  t(s,a,{x:0.6,y,w:1.5,h:0.34,fontFace:B,fontSize:13,bold:true,color:NAVY});
  t(s,b2,{x:2.15,y,w:10.5,h:0.34,fontFace:B,fontSize:13,color:INK});});
t(s,'Более 80% собранных корзин не оплачиваются. +1 п.п. на этом шаге = +5 продаж в месяц без рубля рекламы.',
  {x:0.6,y:6.85,w:12.1,h:0.4,fontFace:B,fontSize:13,italic:true,color:GREY});
s.addNotes('Самый дешёвый резерв роста лежит не в рекламе, а в оплате корзины: брошенные корзины, рассрочка, бесплатная доставка от 3 000 ₽.');

/* 10 — решение */
s=p.addSlide(); head(s,'Решение: бюджет следующего месяца','54 000 ₽ → 62 000 ₽. Доля канала меняется пропорционально его ROAS');
s.addChart(p.ChartType.bar,[
  {name:'Было',labels:CH,values:[5000,12000,12000,15000,10000]},
  {name:'Стало',labels:CH,values:[11634,11736,16244,16569,5817]}],
  Object.assign({},chartBase,{x:0.5,y:1.85,w:8.0,h:4.3,barDir:'col',
   chartColors:['D7DAE0',AMBER],showLegend:true,legendPos:'t',legendFontFace:B,legendFontSize:12,
   dataLabelPosition:'outEnd',dataLabelFormatCode:'#,##0',dataLabelFontSize:10}));
[['+6 634 ₽','сайт — максимальный рост, потолок модели ×2'],
 ['+4 244 ₽','LaModa — берёт объём немедленно'],
 ['−4 183 ₽','ВК — сокращаем вдвое, в ноль не выключаем']]
 .forEach(([a,b2],i)=>{const y=2.15+i*1.4;
  t(s,a,{x:8.9,y,w:3.8,h:0.4,fontFace:B,fontSize:20,bold:true,color:i===2?RED:NAVY});
  t(s,b2,{x:8.9,y:y+0.42,w:3.8,h:0.8,fontFace:B,fontSize:12,color:GREY});});
t(s,'Поправка к модели: сайту нельзя «выдать» 11 634 ₽ и получить трафик завтра — SEO даёт эффект через 2–3 месяца.',
  {x:0.6,y:6.35,w:12.1,h:0.4,fontFace:B,fontSize:13,italic:true,color:GREY});
s.addNotes('Модель предложила раскладку, мы поправили её руками — это и есть управленческое решение, а не арифметика.');

/* 11 — план */
s=p.addSlide(); head(s,'Что делаем в следующем месяце');
[['1','Снимаем 4 200 ₽ с ВК','ДРР 42%, CAC 1 429 ₽ при марже 1 763 ₽. Любое масштабирование уведёт канал в минус.'],
 ['2','Отдаём их в LaModa','Единственный канал, который конвертирует деньги в объём сразу, без лага.'],
 ['3','SEO наращиваем плавно','Бюджет сайта поднимаем поэтапно: отдача приходит через 2–3 месяца, разом её не купить.'],
 ['4','Блогеров — на процент','Убираем фикс 15 000 ₽ вперёд: бартер или % с промокода. Риск уходит с нас.']]
 .forEach(([n,a,b2],i)=>{const x=0.6+(i%2)*6.25, y=1.8+Math.floor(i/2)*2.35;
  card(s,x,y,5.85,2.0);
  circle(s,x+0.4,y+0.35,0.5);
  t(s,n,{x:x+0.4,y:y+0.43,w:0.5,h:0.34,fontFace:B,fontSize:17,bold:true,color:NAVY,align:'center'});
  t(s,a,{x:x+1.05,y:y+0.38,w:4.5,h:0.4,fontFace:B,fontSize:16,bold:true,color:NAVY});
  t(s,b2,{x:x+1.05,y:y+0.85,w:4.5,h:0.95,fontFace:B,fontSize:12,color:GREY});});
t(s,'Общий бюджет не растёт сверх плановых +15%. Все движения — внутри, за счёт слабого канала.',
  {x:0.6,y:6.65,w:12.1,h:0.4,fontFace:B,fontSize:13,italic:true,color:GREY});
s.addNotes('Четыре действия, каждое обосновано цифрой из таблицы.');

/* 12 — финал */
s=p.addSlide(); s.background={color:NAVY};
s.addShape(p.ShapeType.ellipse,{x:-1.6,y:4.2,w:5.0,h:5.0,fill:{color:AMBER,transparency:90},line:{type:'none'}});
t(s,'Деньги приносит LaModa.\nЭффективность даёт сайт.\nЭто разные роли.',
  {x:0.9,y:1.6,w:11.5,h:2.6,fontFace:H,fontSize:38,bold:true,color:W,lineSpacing:50});
t(s,'Бюджет должен это учитывать: объём покупаем на площадке, маржу растим у себя.',
  {x:0.9,y:4.35,w:11.5,h:0.45,fontFace:B,fontSize:17,color:AMBER});
[['85 457 ₽','в кассе за месяц'],['2,58','маржи на рубль'],['0','убыточных каналов']]
 .forEach(([v,l],i)=>{const x=0.9+i*3.9;
  t(s,v,{x,y:5.35,w:3.6,h:0.6,fontFace:B,fontSize:28,bold:true,color:W});
  t(s,l,{x,y:6.0,w:3.6,h:0.35,fontFace:B,fontSize:12,color:DIM});});
s.addNotes('Финальный тезис. Дальше — вопросы.');

p.writeFile({fileName:'Кейс2_Питч_каналы_продаж.pptx'}).then(f=>console.log('OK',f));
