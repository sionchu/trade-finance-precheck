import type { FrontendRendererArgs } from "@streamlit/component-v2-lib";
import { ArrowLeftRight, FileCheck2, FileText, Landmark, SlidersHorizontal } from "lucide-react";
import { AnimatePresence, motion, MotionConfig } from "motion/react";
import { useEffect, useState, type ComponentType, type ReactElement } from "react";

export type StageId = "deal" | "liquidity" | "treasury" | "review" | "result";
export type ReviewGoal = "overall" | "liquidity" | "fx" | "funding";
export type ResponseAction = "none" | "price" | "receivable" | "credit" | "forward" | "usance";
type StageState = "complete" | "ready" | "blocked";
type Stage = { id: StageId; label: string; state: StageState };
type Choice<T> = { id: T; label: string };
type SnapshotCard = { label: string; value: string; detail: string; status: "neutral" | "success" | "warning" | "danger" };
export type ExperienceData = {
  product: { title: string; subtitle: string }; stages: Stage[]; snapshot: SnapshotCard[];
  insight: { deal: string; company: string; afterCredit: string }; activeStage: StageId;
  reviewGoal: ReviewGoal; responseAction: ResponseAction; reviewGoals: Choice<ReviewGoal>[];
  responseActions: Choice<Exclude<ResponseAction, "none">>[];
  dealFacts: { label: string; value: string; source: string }[];
  reviewState: { ready?: boolean; hasResult?: boolean; current?: boolean; loading?: boolean; headline?: string; summary?: string; usedTools?: string[]; error?: string };
};
export type ExperienceState = { active_stage: StageId; review_goal: ReviewGoal; response_action: ResponseAction; primary_action?: "run_review" };
type Tools = Pick<FrontendRendererArgs<ExperienceState, ExperienceData>, "setStateValue" | "setTriggerValue">;
const icons: Record<StageId, ComponentType<{ size?: number; "aria-hidden"?: boolean }>> = { deal: FileText, liquidity: Landmark, treasury: ArrowLeftRight, review: SlidersHorizontal, result: FileCheck2 };
const guidance: Record<StageId, string> = {
  deal: "입력 방법을 선택하고 거래를 확인합니다.",
  liquidity: "거래와 회사의 기존 자금계획을 같은 시점에서 확인합니다.",
  treasury: "한 조건을 바꾸고 득실을 비교합니다.",
  review: "목표·환율·조달 가정을 조절해 보세요.",
  result: "현재 입력 기준 결과",
};

export default function ExperienceShell({ data, setStateValue, setTriggerValue }: Tools & { data: ExperienceData }): ReactElement {
  const [activeStage, setActiveStage] = useState<StageId>(data.activeStage);
  useEffect(() => setActiveStage(data.activeStage), [data.activeStage]);
  const navigate = (stage: StageId): void => { setActiveStage(stage); setStateValue("active_stage", stage); };
  const selectStage = (stage: Stage): void => { if (stage.state !== "blocked") navigate(stage.id); };
  const runReview = (): void => { navigate("result"); setTriggerValue("primary_action", "run_review"); };
  return <MotionConfig reducedMotion="user" transition={{ duration: 0.2 }}>
    <section className="experience" aria-label={data.product.title}>

      <nav className="stages" aria-label="사전점검 단계">{data.stages.map(stage => { const Icon=icons[stage.id]; const selected=activeStage===stage.id; return <button className={`stage stage--${selected?"active":stage.state}`} type="button" key={stage.id} disabled={stage.state==="blocked"} aria-current={selected?"step":undefined} onClick={()=>selectStage(stage)}><Icon size={19} aria-hidden/><span>{stage.label}</span>{selected&&<motion.span className="stage-indicator" layoutId="stage-indicator"/>}</button>; })}</nav>
      <AnimatePresence mode="wait"><motion.div className="stage-panel" key={activeStage} initial={{opacity:0,y:6}} animate={{opacity:1,y:0}} exit={{opacity:0}}>
        <h2>{guidance[activeStage]}</h2>
        {activeStage==="deal"&&<><details><summary>현재 거래 요약</summary><div className="fact-grid">{data.dealFacts.map(f=><div key={f.label}><span>{f.label}</span><strong>{f.value}</strong><small>{f.source}</small></div>)}</div></details><button className="primary-action" type="button" onClick={()=>navigate("review")}>판단 기준 조절</button></>}
        {activeStage==="liquidity"&&<><div className="insight"><div><span>거래만 본 은행 필요액</span><strong>{data.insight.deal}</strong></div><div><span>회사 자금계획 포함 Peak 부족</span><strong>{data.insight.company}</strong></div><div><span>미사용 한도 적용 후</span><strong>{data.insight.afterCredit}</strong></div></div><p className="support">회사 기존 지급계획을 합쳐 같은 날짜의 부족액을 비교합니다.</p><button className="primary-action" type="button" onClick={()=>navigate("treasury")}>대응 시뮬레이션</button></>}
        {activeStage==="treasury"&&<button className="primary-action" type="button" onClick={()=>navigate("result")}>결과·보고서 확인</button>}
        {activeStage==="review"&&<><p className="support">아래 조절값은 계산에 즉시 반영됩니다.</p><button className="primary-action" type="button" onClick={()=>navigate("liquidity")}>회사 자금 확인</button></>}
        {activeStage==="result"&&<>
          <div className="decision-snapshot">{data.snapshot.map(card=><div key={card.label}><span>{card.label}</span><strong>{card.value}</strong><small>{card.detail}</small></div>)}</div>
          <h3>거래 검토 요약</h3>
          {data.reviewState.loading?<p>현재 거래 근거를 확인하고 있습니다.</p>:data.reviewState.error?<p className="error">{data.reviewState.error}</p>:data.reviewState.current?<><h3>{data.reviewState.headline}</h3><p>{data.reviewState.summary}</p><details><summary>상세 설명 보기</summary><small>확인 완료 · {data.reviewState.usedTools?.join(" · ")}</small></details></>:data.reviewState.hasResult?<p>조건이 변경되어 다시 검토가 필요합니다.</p>:<p className="support">현재 계산의 의미를 짧게 검토할 수 있습니다.</p>}
          <button className="primary-action" type="button" disabled={!data.reviewState.ready} onClick={runReview}>이 조건으로 거래 검토</button>
        </>}
      </motion.div></AnimatePresence>
    </section>
  </MotionConfig>;
}
